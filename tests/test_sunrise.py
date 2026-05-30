"""Tests for the sunrise module."""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from homeassistant.core import Context, HomeAssistant, State

from custom_components.adaptive_lighting.sunrise import (
    LIGHT_SUPPORT_BRIGHTNESS,
    LIGHT_SUPPORT_CCT,
    LIGHT_SUPPORT_RGB,
    SUNRISE_SCHEMA,
    SunriseSequence,
    _lerp,
    _lerp_rgb,
)


def test_lerp():
    assert _lerp(0, 100, 0.5) == 50
    assert _lerp(10, 20, 0.0) == 10
    assert _lerp(10, 20, 1.0) == 20
    assert _lerp(0, 100, 0.25) == 25


def test_lerp_rgb():
    assert _lerp_rgb((0, 0, 0), (255, 255, 255), 0.5) == (127, 127, 127)
    assert _lerp_rgb((0, 0, 0), (255, 255, 255), 0.0) == (0, 0, 0)
    assert _lerp_rgb((0, 0, 0), (255, 255, 255), 1.0) == (255, 255, 255)


def test_sunrise_rgb_color():
    seq = _make_seq()
    assert seq._sunrise_rgb_color(0.0) == (255, 20, 0)
    assert seq._sunrise_rgb_color(0.15) == (255, 100, 0)
    assert seq._sunrise_rgb_color(0.25) == (255, 160, 30)
    assert seq._sunrise_rgb_color(0.50) == (255, 190, 70)


def test_init_sets_defaults():
    seq = _make_seq()
    assert seq.duration == 15
    assert seq.hold_time == 5
    assert seq.max_brightness == 70
    assert seq.target_color_temp == 4000
    assert seq._cancelled is False
    assert seq._task is None
    assert seq._manual_lights == set()


def test_detect_light_capabilities_no_state():
    seq = _make_seq()
    seq.hass.states.get = Mock(return_value=None)
    assert seq._detect_light_capabilities("light.nonexistent") == set()


def test_detect_light_capabilities_rgb_only():
    seq = _make_seq()
    seq.hass.states.get = Mock(return_value=State("light.test", "on", attributes={"supported_color_modes": ["rgb"]}))
    assert seq._detect_light_capabilities("light.test") == LIGHT_SUPPORT_RGB


def test_detect_light_capabilities_cct_only():
    seq = _make_seq()
    seq.hass.states.get = Mock(return_value=State("light.test", "on", attributes={"supported_color_modes": ["color_temp"]}))
    assert seq._detect_light_capabilities("light.test") == LIGHT_SUPPORT_CCT


def test_detect_light_capabilities_both():
    seq = _make_seq()
    seq.hass.states.get = Mock(return_value=State("light.test", "on", attributes={"supported_color_modes": ["rgb", "color_temp"]}))
    assert seq._detect_light_capabilities("light.test") == LIGHT_SUPPORT_RGB | LIGHT_SUPPORT_CCT


def test_detect_light_capabilities_brightness_only():
    seq = _make_seq()
    seq.hass.states.get = Mock(return_value=State("light.test", "on", attributes={"supported_color_modes": ["brightness"]}))
    assert seq._detect_light_capabilities("light.test") == {"brightness"}


def test_on_state_changed_ignores_own_context():
    seq = _make_seq()
    event = Mock()
    event.data = {"entity_id": "light.test", "new_state": State("light.test", "on"), "old_state": State("light.test", "off")}
    event.data["new_state"].context = seq.context
    seq._on_state_changed(event)
    assert "light.test" not in seq._manual_lights


def test_on_state_changed_tracks_external_change():
    seq = _make_seq()
    event = Mock()
    event.data = {"entity_id": "light.test", "new_state": State("light.test", "on"), "old_state": State("light.test", "off")}
    event.data["new_state"].context = Context(id="external")
    seq._on_state_changed(event)
    assert "light.test" in seq._manual_lights


def test_on_state_changed_ignores_unknown_light():
    seq = _make_seq()
    event = Mock()
    event.data = {"entity_id": "light.other", "new_state": State("light.test", "on"), "old_state": State("light.test", "off")}
    seq._on_state_changed(event)
    assert len(seq._manual_lights) == 0


def test_on_state_changed_ignores_already_tracked():
    seq = _make_seq()
    seq._manual_lights.add("light.test")
    event = Mock()
    event.data = {"entity_id": "light.test", "new_state": State("light.test", "on"), "old_state": State("light.test", "off")}
    seq._on_state_changed(event)
    assert len(seq._manual_lights) == 1


def test_on_state_changed_ignores_none_state():
    seq = _make_seq()
    event = Mock()
    event.data = {"entity_id": "light.test", "new_state": None, "old_state": None}
    seq._on_state_changed(event)
    assert len(seq._manual_lights) == 0


def test_remove_listener():
    seq = _make_seq()
    seq._unsub_listener = Mock()
    seq._remove_listener()
    assert seq._unsub_listener is None


def test_cancel():
    seq = _make_seq()
    seq._task = AsyncMock()
    seq._unsub_listener = Mock()
    seq.cancel()
    assert seq._cancelled is True
    seq._task.cancel.assert_called_once()
    seq._unsub_listener.assert_called_once()


def test_cancel_no_task():
    seq = _make_seq()
    seq._unsub_listener = Mock()
    seq.cancel()
    assert seq._cancelled is True
    seq._unsub_listener.assert_called_once()


@pytest.mark.asyncio
async def test_run_phases_in_order():
    seq = _make_seq()
    phases_run = []
    async def ps(): phases_run.append("sunrise")
    async def ph(): phases_run.append("hold")
    async def psh(): phases_run.append("shutdown")
    seq._phase_sunrise = ps
    seq._phase_hold = ph
    seq._phase_shutdown = psh
    seq.lights = ["light.test"]
    seq._detect_light_capabilities = Mock(return_value=set())
    await seq._run()
    assert phases_run == ["sunrise", "hold", "shutdown"]


@pytest.mark.asyncio
async def test_run_cancelled_after_sunrise():
    seq = _make_seq()
    phases_run = []
    async def ps():
        phases_run.append("sunrise")
        seq._cancelled = True
    seq._phase_sunrise = ps
    seq._phase_hold = AsyncMock()
    seq._phase_shutdown = AsyncMock()
    seq.lights = ["light.test"]
    seq._detect_light_capabilities = Mock(return_value=set())
    await seq._run()
    assert phases_run == ["sunrise"]
    seq._phase_hold.assert_not_called()
    seq._phase_shutdown.assert_not_called()


@pytest.mark.asyncio
async def test_run_skipped_without_lights():
    seq = _make_seq()
    seq.lights = []
    seq._phase_sunrise = AsyncMock()
    await seq._run()
    seq._phase_sunrise.assert_not_called()


@pytest.mark.asyncio
async def test_start_binds_listener_and_awaits(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._detect_light_capabilities = Mock(return_value=set())
    seq._phase_sunrise = AsyncMock()
    seq._phase_hold = AsyncMock()
    seq._phase_shutdown = AsyncMock()
    await seq.start()
    assert seq._task is not None


@pytest.mark.asyncio
async def test_start_cancellation(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._detect_light_capabilities = Mock(return_value=set())
    async def ps(): raise asyncio.CancelledError()
    seq._phase_sunrise = ps
    with pytest.raises(asyncio.CancelledError):
        await seq.start()


@pytest.mark.asyncio
async def test_phase_sunrise_with_rgb_lights(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._lights_data = {"light.test": {"capabilities": {"color", "brightness"}}}
    seq.step_interval = 0.001
    seq.total_steps = 3
    seq.duration = 1
    calls = []
    async def capture(*a, **kw): calls.append((a, kw))
    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_sunrise()


@pytest.mark.asyncio
async def test_phase_sunrise_skips_manual_lights(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.manual", "light.auto"]
    seq._manual_lights.add("light.manual")
    seq._lights_data = {"light.manual": {"capabilities": {"color_temp", "brightness"}}, "light.auto": {"capabilities": {"color_temp", "brightness"}}}
    seq.step_interval = 0.001
    seq.total_steps = 2
    seq.duration = 0.1
    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_sunrise()


@pytest.mark.asyncio
async def test_phase_sunrise_cancelled(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._lights_data = {"light.test": {"capabilities": {"color_temp", "brightness"}}}
    seq._cancelled = True
    await seq._phase_sunrise()


@pytest.mark.asyncio
async def test_phase_hold_no_hold_time():
    seq = _make_seq()
    seq.hold_time = 0
    await seq._phase_hold()


@pytest.mark.asyncio
async def test_phase_hold_sends_commands(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._lights_data = {"light.test": {"capabilities": {"color_temp", "brightness"}}}
    seq.hold_time = 0.001
    calls = []
    async def capture(*a, **kw): calls.append((a, kw))
    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_hold()
    assert len(calls) > 0


@pytest.mark.asyncio
async def test_phase_hold_skips_manual_lights(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.manual", "light.auto"]
    seq._manual_lights.add("light.manual")
    seq._lights_data = {"light.manual": {"capabilities": {"color_temp", "brightness"}}, "light.auto": {"capabilities": {"color_temp", "brightness"}}}
    seq.hold_time = 0.001
    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_hold()


@pytest.mark.asyncio
async def test_phase_shutdown_dims_and_turns_off(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._lights_data = {"light.test": {"capabilities": {"color_temp", "brightness"}}}
    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_shutdown()


@pytest.mark.asyncio
async def test_phase_shutdown_skips_manual_lights(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.manual", "light.auto"]
    seq._manual_lights.add("light.manual")
    seq._lights_data = {"light.manual": {"capabilities": {"color_temp", "brightness"}}, "light.auto": {"capabilities": {"color_temp", "brightness"}}}
    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_shutdown()


@pytest.mark.asyncio
async def test_phase_shutdown_cancelled(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._lights_data = {"light.test": {"capabilities": {"color_temp", "brightness"}}}
    seq._cancelled = True
    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_shutdown()


@pytest.mark.asyncio
async def test_async_register_service(hass):
    SunriseSequence.async_register_service(hass)
    assert hass.services.has_service("adaptive_lighting", "sunrise")


def test_sunrise_schema_valid():
    assert SUNRISE_SCHEMA is not None
    keys = list(SUNRISE_SCHEMA.schema.keys())
    assert "lights" in keys
    assert "sunrise_duration" in keys
    assert "sunrise_hold_time" in keys


def _make_seq():
    ctx = Context(id="test-sunrise-ctx")
    hass = Mock()
    hass.services.async_call = AsyncMock()
    hass.states.get = Mock()
    hass.bus.async_listen = Mock(return_value=Mock())
    return SunriseSequence(
        hass=hass,
        context=ctx,
        lights=["light.test"],
        duration=15,
        hold_time=5,
        max_brightness=70,
        target_color_temp=4000,
        min_color_temp=2000,
        rgb_threshold=2500,
        transition=30,
    )
