"""Sunrise simulation for Adaptive Lighting.

Runs a configurable sunrise sequence on a set of lights, transitioning
from warm RGB colors through CCT to simulate a natural sunrise.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from typing import Any

import voluptuous as vol
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP_KELVIN,
    ATTR_RGB_COLOR,
    ATTR_TRANSITION,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)
from homeassistant.components.light import (
    DOMAIN as LIGHT_DOMAIN,
)
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import Context, Event, HomeAssistant, ServiceCall, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.util.color import color_temperature_to_rgb

from .const import (
    CONF_LIGHTS,
    CONF_SUNRISE_DURATION,
    CONF_SUNRISE_HOLD_TIME,
    CONF_SUNRISE_MAX_BRIGHTNESS,
    CONF_SUNRISE_MIN_COLOR_TEMP,
    CONF_SUNRISE_RGB_THRESHOLD,
    CONF_SUNRISE_TARGET_COLOR_TEMP,
    CONF_SUNRISE_TRANSITION,
    DEFAULT_SUNRISE_DURATION,
    DEFAULT_SUNRISE_HOLD_TIME,
    DEFAULT_SUNRISE_MAX_BRIGHTNESS,
    DEFAULT_SUNRISE_MIN_COLOR_TEMP,
    DEFAULT_SUNRISE_RGB_THRESHOLD,
    DEFAULT_SUNRISE_TARGET_COLOR_TEMP,
    DEFAULT_SUNRISE_TRANSITION,
    DOMAIN,
    SERVICE_SUNRISE,
)

SUNRISE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_LIGHTS): cv.entity_ids,
        vol.Optional(
            CONF_SUNRISE_DURATION,
            default=DEFAULT_SUNRISE_DURATION,
        ): cv.positive_int,
        vol.Optional(
            CONF_SUNRISE_HOLD_TIME,
            default=DEFAULT_SUNRISE_HOLD_TIME,
        ): cv.positive_int,
        vol.Optional(
            CONF_SUNRISE_MAX_BRIGHTNESS,
            default=DEFAULT_SUNRISE_MAX_BRIGHTNESS,
        ): vol.All(vol.Coerce(int), vol.Range(min=1, max=100)),
        vol.Optional(
            CONF_SUNRISE_TARGET_COLOR_TEMP,
            default=DEFAULT_SUNRISE_TARGET_COLOR_TEMP,
        ): vol.All(vol.Coerce(int), vol.Range(min=1000, max=10000)),
        vol.Optional(
            CONF_SUNRISE_MIN_COLOR_TEMP,
            default=DEFAULT_SUNRISE_MIN_COLOR_TEMP,
        ): vol.All(vol.Coerce(int), vol.Range(min=1000, max=10000)),
        vol.Optional(
            CONF_SUNRISE_RGB_THRESHOLD,
            default=DEFAULT_SUNRISE_RGB_THRESHOLD,
        ): vol.All(vol.Coerce(int), vol.Range(min=1000, max=10000)),
        vol.Optional(
            CONF_SUNRISE_TRANSITION,
            default=DEFAULT_SUNRISE_TRANSITION,
        ): vol.All(vol.Coerce(int), vol.Range(min=1, max=300)),
    },
)

LIGHT_SUPPORT_RGB = {"color", "brightness"}
LIGHT_SUPPORT_CCT = {"color_temp", "brightness"}
LIGHT_SUPPORT_BRIGHTNESS = {"brightness"}

_LOGGER = logging.getLogger(__name__)


def _lerp(start: float, end: float, progress: float) -> float:
    return start + (end - start) * progress


def _lerp_rgb(
    start: tuple[int, int, int],
    end: tuple[int, int, int],
    progress: float,
) -> tuple[int, int, int]:
    return (
        round(_lerp(start[0], end[0], progress)),
        round(_lerp(start[1], end[1], progress)),
        round(_lerp(start[2], end[2], progress)),
    )


class SunriseSequence:
    """Orchestrates a sunrise simulation on a set of lights."""

    def __init__(
        self,
        hass: HomeAssistant,
        context: Context,
        lights: list[str],
        duration: int,
        hold_time: int,
        max_brightness: int,
        target_color_temp: int,
        min_color_temp: int,
        rgb_threshold: int,
        transition: int,
    ) -> None:
        """Initialize the sunrise sequence."""
        self.hass = hass
        self.context = context
        self.lights = lights
        self.duration = duration
        self.hold_time = hold_time
        self.max_brightness = max_brightness
        self.target_color_temp = target_color_temp
        self.min_color_temp = min_color_temp
        self.rgb_threshold = rgb_threshold
        self.transition = transition

        self.step_interval = 15
        self.total_steps = max(1, (duration * 60) // self.step_interval)
        self._lights_data: dict[str, dict[str, Any]] = {}
        self._cancelled = False
        self._task: asyncio.Task | None = None
        self._manual_lights: set[str] = set()
        self._unsub_listener: Callable[[], None] | None = None

    @callback
    def _on_state_changed(self, event: Event) -> None:
        """Track state changes on lights to detect manual interruptions."""
        entity_id = event.data.get("entity_id", "")
        if entity_id not in self.lights:
            return
        if entity_id in self._manual_lights:
            return
        new_state = event.data.get("new_state")
        old_state = event.data.get("old_state")
        if new_state is None or old_state is None:
            return
        if new_state.context.id == self.context.id:
            return
        self._manual_lights.add(entity_id)
        _LOGGER.debug(
            "Light '%s' was manually changed during sunrise sequence,"
            " moving it to manual_lights set",
            entity_id,
        )

    def _remove_listener(self) -> None:
        """Remove the state_changed event listener."""
        if self._unsub_listener is not None:
            self._unsub_listener()
            self._unsub_listener = None

    @callback
    def cancel(self) -> None:
        """Cancel the running sequence."""
        self._cancelled = True
        self._remove_listener()
        if self._task is not None:
            self._task.cancel()

    def _detect_light_capabilities(self, light: str) -> set[str]:
        """Detect what a light supports."""
        state = self.hass.states.get(light)
        if state is None:
            return set()
        supported = set()
        attrs = state.attributes
        supported_modes = attrs.get("supported_color_modes", [])
        color_modes = {"rgb", "rgbw", "rgbww", "xy", "hs"}
        if any(m in supported_modes for m in color_modes):
            supported.update(LIGHT_SUPPORT_RGB)
        if "color_temp" in supported_modes:
            supported.update(LIGHT_SUPPORT_CCT)
        if "brightness" in supported_modes:
            supported.add("brightness")
        return supported

    async def start(self) -> None:
        """Start the sunrise sequence."""
        self._unsub_listener = self.hass.bus.async_listen(
            "state_changed",
            self._on_state_changed,
        )
        self._task = asyncio.create_task(self._run())
        try:
            await self._task
        except asyncio.CancelledError:
            _LOGGER.debug("Sunrise sequence cancelled")
            raise
        finally:
            self._remove_listener()

    async def _run(self) -> None:
        _LOGGER.debug(
            "Starting sunrise sequence: %d lights, %d min duration, %d min hold",
            len(self.lights),
            self.duration,
            self.hold_time,
        )
        for light in self.lights:
            capabilities = self._detect_light_capabilities(light)
            self._lights_data[light] = {"capabilities": capabilities}

        if not self.lights:
            return

        await self._phase_sunrise()
        if self._cancelled:
            return
        await self._phase_hold()
        if self._cancelled:
            return
        await self._phase_shutdown()

    def _sunrise_rgb_color(self, progress: float) -> tuple[int, int, int]:
        """Compute RGB color for the warm sunrise phase (progress 0.0~0.35)."""
        deep_red = (255, 20, 0)
        orange = (255, 100, 0)
        golden = (255, 160, 30)
        warm_amber = (255, 190, 70)

        if progress < 0.15:
            p = progress / 0.15
            return _lerp_rgb(deep_red, orange, p)
        if progress < 0.25:
            p = (progress - 0.15) / 0.1
            return _lerp_rgb(orange, golden, p)
        p = (progress - 0.25) / 0.1
        return _lerp_rgb(golden, warm_amber, p)

    async def _phase_sunrise(self) -> None:
        """Run the sunrise ramp (RGB warm-up + CCT ramp)."""
        duration_sec = self.duration * 60
        steps = self.total_steps
        rgb_duration_ratio = 0.35
        transition_duration_ratio = 0.10
        cct_start_ratio = rgb_duration_ratio + transition_duration_ratio

        for step in range(steps):
            if self._cancelled:
                return

            progress = (step + 1) / steps
            current_brightness_pct = _lerp(1, self.max_brightness, progress)
            brightness = round(255 * current_brightness_pct / 100)

            total_elapsed = ((step + 1) / steps) * duration_sec
            remaining = duration_sec - total_elapsed
            current_transition = min(
                self.transition,
                max(1, round(remaining / (steps - step))),
            )

            tasks = []
            for light in self.lights:
                if light in self._manual_lights:
                    continue
                caps = self._lights_data[light]["capabilities"]
                service_data: dict[str, Any] = {ATTR_ENTITY_ID: light}

                if LIGHT_SUPPORT_RGB.issubset(caps) and progress < cct_start_ratio:
                    rgb = self._sunrise_rgb_color(progress)
                    service_data[ATTR_RGB_COLOR] = list(rgb)
                elif LIGHT_SUPPORT_CCT.issubset(caps) or (
                    LIGHT_SUPPORT_RGB.issubset(caps) and progress >= cct_start_ratio
                ):
                    if progress < cct_start_ratio:
                        temp = self.min_color_temp
                    else:
                        cct_progress = (progress - cct_start_ratio) / (
                            1 - cct_start_ratio
                        )
                        temp = round(
                            _lerp(
                                self.rgb_threshold,
                                self.target_color_temp,
                                cct_progress,
                            ),
                        )
                        temp = max(temp, self.min_color_temp)
                    service_data[ATTR_COLOR_TEMP_KELVIN] = temp
                elif "brightness" not in caps:
                    continue

                if "brightness" in caps:
                    service_data[ATTR_BRIGHTNESS] = brightness

                if current_transition > 0:
                    service_data[ATTR_TRANSITION] = current_transition

                if len(service_data) > 1:
                    tasks.append(
                        self.hass.services.async_call(
                            LIGHT_DOMAIN,
                            SERVICE_TURN_ON,
                            service_data,
                            context=self.context,
                        ),
                    )

            if tasks:
                await asyncio.gather(*tasks)

            sleep_time = self.step_interval
            await asyncio.sleep(sleep_time)

    async def _phase_hold(self) -> None:
        """Hold lights at max settings."""
        if self.hold_time <= 0:
            return

        target_brightness = round(255 * self.max_brightness / 100)

        tasks = []
        for light in self.lights:
            if light in self._manual_lights:
                continue
            caps = self._lights_data[light]["capabilities"]
            service_data: dict[str, Any] = {
                ATTR_ENTITY_ID: light,
                ATTR_TRANSITION: 5,
            }
            if LIGHT_SUPPORT_CCT.issubset(caps):
                service_data[ATTR_COLOR_TEMP_KELVIN] = self.target_color_temp
            elif LIGHT_SUPPORT_RGB.issubset(caps):
                rgb = color_temperature_to_rgb(self.target_color_temp)
                service_data[ATTR_RGB_COLOR] = [
                    round(rgb[0]),
                    round(rgb[1]),
                    round(rgb[2]),
                ]
            if "brightness" in caps:
                service_data[ATTR_BRIGHTNESS] = target_brightness
            if len(service_data) > 1:
                tasks.append(
                    self.hass.services.async_call(
                        LIGHT_DOMAIN,
                        SERVICE_TURN_ON,
                        service_data,
                        context=self.context,
                    ),
                )

        if tasks:
            await asyncio.gather(*tasks)

        await asyncio.sleep(self.hold_time * 60)

    async def _phase_shutdown(self) -> None:
        """Gracefully dim lights down and turn off."""
        dim_steps = 5
        for step in range(dim_steps, 0, -1):
            if self._cancelled:
                return

            brightness_pct = _lerp(0, self.max_brightness, (step - 1) / dim_steps)
            if step == 1:
                brightness_pct = 0

            brightness = round(255 * brightness_pct / 100)
            transition = 3

            tasks = []
            for light in self.lights:
                if light in self._manual_lights:
                    continue
                caps = self._lights_data[light]["capabilities"]
                service_data: dict[str, Any] = {
                    ATTR_ENTITY_ID: light,
                    ATTR_TRANSITION: transition,
                }
                if step > 1 and "brightness" in caps:
                    service_data[ATTR_BRIGHTNESS] = brightness
                if len(service_data) <= 1:
                    continue
                tasks.append(
                    self.hass.services.async_call(
                        LIGHT_DOMAIN,
                        SERVICE_TURN_ON if step > 1 else SERVICE_TURN_OFF,
                        service_data if step > 1 else {ATTR_ENTITY_ID: light},
                        context=self.context,
                    ),
                )

            if tasks:
                await asyncio.gather(*tasks)

            await asyncio.sleep(transition)

    @staticmethod
    @callback
    def async_register_service(hass: HomeAssistant) -> None:
        """Register the sunrise service."""

        async def handle_sunrise(service_call: ServiceCall) -> None:
            data = service_call.data
            lights = data[CONF_LIGHTS]
            duration = data[CONF_SUNRISE_DURATION]
            hold_time = data[CONF_SUNRISE_HOLD_TIME]
            max_brightness = data[CONF_SUNRISE_MAX_BRIGHTNESS]
            target_color_temp = data[CONF_SUNRISE_TARGET_COLOR_TEMP]
            min_color_temp = data[CONF_SUNRISE_MIN_COLOR_TEMP]
            rgb_threshold = data[CONF_SUNRISE_RGB_THRESHOLD]
            transition = data[CONF_SUNRISE_TRANSITION]

            sequence = SunriseSequence(
                hass=hass,
                context=service_call.context,
                lights=lights,
                duration=duration,
                hold_time=hold_time,
                max_brightness=max_brightness,
                target_color_temp=target_color_temp,
                min_color_temp=min_color_temp,
                rgb_threshold=rgb_threshold,
                transition=transition,
            )

            hass.async_create_task(sequence.start())

        hass.services.async_register(
            domain=DOMAIN,
            service=SERVICE_SUNRISE,
            service_func=handle_sunrise,
            schema=SUNRISE_SCHEMA,
        )
