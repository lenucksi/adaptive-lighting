"""Tests for the sunrise module."""

import asyncio
from unittest.mock import AsyncMock, Mock

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
    black = (0, 0, 0)
    white = (255, 255, 255)
    mid = _lerp_rgb(black, white, 0.5)
    assert mid == (127, 127, 127)
    assert _lerp_rgb(black, white, 0.0) == (0, 0, 0)
    assert _lerp_rgb(black, white, 1.0) == (255, 255, 255)


def test_sunrise_rgb_color():
    seq = _make_seq()
    deep_red = (255, 20, 0)
    orange = (255, 100, 0)
    golden = (255, 160, 30)
    warm_amber = (255, 190, 70)

    assert seq._sunrise_rgb_color(0.0) == deep_red
    color_at_15 = seq._sunrise_rgb_color(0.15)
    assert color_at_15 == orange
    color_at_25 = seq._sunrise_rgb_color(0.25)
    assert color_at_25 == golden
    color_at_50 = seq._sunrise_rgb_color(0.50)
    assert color_at_50 == warm_amber


def test_init_sets_defaults():
    seq = _make_seq()
    assert seq.duration == 15
    assert seq.hold_time == 5
    assert seq.max_brightness == 70
    assert seq.target_color_temp == 4000
    assert seq.min_color_temp == 2000
    assert seq.rgb_threshold == 2500
    assert seq.transition == 30
    assert seq.step_interval == 15
    assert seq.total_steps == 60
    assert seq._lights_data == {}
    assert seq._cancelled is False
    assert seq._task is None
    assert seq._manual_lights == set()


def test_detect_light_capabilities_no_state():
    seq = _make_seq()
    seq.hass.states.get = Mock(return_value=None)
    result = seq._detect_light_capabilities("light.nonexistent")
    assert result == set()


def test_detect_light_capabilities_rgb_only():
    seq = _make_seq()
    state = State("light.test", "on", attributes={"supported_color_modes": ["rgb"]})
    seq.hass.states.get = Mock(return_value=state)
    result = seq._detect_light_capabilities("light.test")
    assert result == LIGHT_SUPPORT_RGB


def test_detect_light_capabilities_cct_only():
    seq = _make_seq()
    state = State("light.test", "on", attributes={"supported_color_modes": ["color_temp"]})
    seq.hass.states.get = Mock(return_value=state)
    result = seq._detect_light_capabilities("light.test")
    assert result == LIGHT_SUPPORT_CCT


def test_detect_light_capabilities_both():
    seq = _make_seq()
    state = State(
        "light.test", "on",
        attributes={"supported_color_modes": ["rgb", "color_temp"]},
    )
    seq.hass.states.get = Mock(return_value=state)
    result = seq._detect_light_capabilities("light.test")
    assert result == LIGHT_SUPPORT_RGB | LIGHT_SUPPORT_CCT


def test_detect_light_capabilities_brightness_only():
    seq = _make_seq()
    state = State("light.test", "on", attributes={"supported_color_modes": ["brightness"]})
    seq.hass.states.get = Mock(return_value=state)
    result = seq._detect_light_capabilities("light.test")
    assert result == {"brightness"}


def test_on_state_changed_ignores_own_context():
    seq = _make_seq()
    event = Mock()
    event.data = {
        "entity_id": "light.test",
        "new_state": State("light.test", "on"),
        "old_state": State("light.test", "off"),
    }
    event.data["new_state"].context = seq.context
    seq._on_state_changed(event)
    assert "light.test" not in seq._manual_lights


def test_on_state_changed_tracks_external_change():
    seq = _make_seq()
    external_ctx = Context(id="external")
    event = Mock()
    event.data = {
        "entity_id": "light.test",
        "new_state": State("light.test", "on"),
        "old_state": State("light.test", "off"),
    }
    event.data["new_state"].context = external_ctx
    seq._on_state_changed(event)
    assert "light.test" in seq._manual_lights


def test_on_state_changed_ignores_unknown_light():
    seq = _make_seq()
    event = Mock()
    event.data = {
        "entity_id": "light.other",
        "new_state": State("light.test", "on"),
        "old_state": State("light.test", "off"),
    }
    seq._on_state_changed(event)
    assert len(seq._manual_lights) == 0


def test_on_state_changed_ignores_already_tracked():
    seq = _make_seq()
    seq._manual_lights.add("light.test")
    event = Mock()
    event.data = {
        "entity_id": "light.test",
        "new_state": State("light.test", "on"),
        "old_state": State("light.test", "off"),
    }
    seq._on_state_changed(event)
    assert len(seq._manual_lights) == 1


def test_on_state_changed_ignores_none_state():
    seq = _make_seq()
    event = Mock()
    event.data = {
        "entity_id": "light.test",
        "new_state": None,
        "old_state": None,
    }
    seq._on_state_changed(event)
    assert len(seq._manual_lights) == 0


def test_remove_listener():
    seq = _make_seq()
    listener = Mock()
    seq._unsub_listener = listener
    seq._remove_listener()
    listener.assert_called_once()
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
    async def phase_sunrise():
        phases_run.append("sunrise")
    async def phase_hold():
        phases_run.append("hold")
    async def phase_shutdown():
        phases_run.append("shutdown")
    seq._phase_sunrise = phase_sunrise
    seq._phase_hold = phase_hold
    seq._phase_shutdown = phase_shutdown
    seq.lights = ["light.test"]
    seq._detect_light_capabilities = Mock(return_value=set())

    await seq._run()
    assert phases_run == ["sunrise", "hold", "shutdown"]


@pytest.mark.asyncio
async def test_run_cancelled_after_sunrise():
    seq = _make_seq()
    phases_run = []
    async def phase_sunrise():
        phases_run.append("sunrise")
        seq._cancelled = True
    seq._phase_sunrise = phase_sunrise
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

    async def phase_sunrise():
        raise asyncio.CancelledError()
    seq._phase_sunrise = phase_sunrise
    seq._phase_hold = AsyncMock()
    seq._phase_shutdown = AsyncMock()

    with pytest.raises(asyncio.CancelledError):
        await seq.start()


@pytest.mark.asyncio
async def test_phase_sunrise_with_rgb_lights(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._lights_data = {
        "light.test": {"capabilities": {"color", "brightness"}},
    }
    seq.step_interval = 0.001
    seq.total_steps = 3
    seq.duration = 1

    service_calls = []
    async def mock_call(domain, service, service_data, context=None):
        service_calls.append((service, service_data))

    seq.hass.services.async_call = mock_call

    await seq._phase_sunrise()
    assert len(service_calls) > 0


@pytest.mark.asyncio
async def test_phase_sunrise_skips_manual_lights(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.manual", "light.auto"]
    seq._manual_lights.add("light.manual")
    seq._lights_data = {
        "light.manual": {"capabilities": {"color_temp", "brightness"}},
        "light.auto": {"capabilities": {"color_temp", "brightness"}},
    }
    seq.step_interval = 0.001
    seq.total_steps = 2
    seq.duration = 0.1

    auto_calls = []
    async def mock_call(domain, service, service_data, context=None):
        if service_data.get("entity_id") == "light.auto":
            auto_calls.append(service)

    seq.hass.services.async_call = mock_call

    await seq._phase_sunrise()
    assert len(auto_calls) > 0


@pytest.mark.asyncio
async def test_phase_sunrise_cancelled(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._lights_data = {
        "light.test": {"capabilities": {"color_temp", "brightness"}},
    }
    seq.step_interval = 0.001
    seq.total_steps = 10
    seq.duration = 1
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
    seq._lights_data = {
        "light.test": {"capabilities": {"color_temp", "brightness"}},
    }
    seq.hold_time = 0.001

    service_calls = []
    async def mock_call(domain, service, service_data, context=None):
        service_calls.append((service, service_data))

    seq.hass.services.async_call = mock_call

    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_hold()
    assert len(service_calls) > 0


@pytest.mark.asyncio
async def test_phase_hold_skips_manual_lights(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.manual", "light.auto"]
    seq._manual_lights.add("light.manual")
    seq._lights_data = {
        "light.manual": {"capabilities": {"color_temp", "brightness"}},
        "light.auto": {"capabilities": {"color_temp", "brightness"}},
    }
    seq.hold_time = 0.001

    auto_calls = []
    async def mock_call(domain, service, service_data, context=None):
        if service_data.get("entity_id") == "light.auto":
            auto_calls.append(service)

    seq.hass.services.async_call = mock_call

    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_hold()
    assert len(auto_calls) > 0


@pytest.mark.asyncio
async def test_phase_shutdown_dims_and_turns_off(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._lights_data = {
        "light.test": {"capabilities": {"color_temp", "brightness"}},
    }

    service_calls = []
    async def mock_call(domain, service, service_data, context=None):
        service_calls.append((service, service_data))

    seq.hass.services.async_call = mock_call

    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_shutdown()
    assert len(service_calls) > 0
    last_call = service_calls[-1]
    assert last_call[0] == "turn_off"


@pytest.mark.asyncio
async def test_phase_shutdown_skips_manual_lights(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.manual", "light.auto"]
    seq._manual_lights.add("light.manual")
    seq._lights_data = {
        "light.manual": {"capabilities": {"color_temp", "brightness"}},
        "light.auto": {"capabilities": {"color_temp", "brightness"}},
    }

    auto_calls = []
    async def mock_call(domain, service, service_data, context=None):
        if service_data.get("entity_id") == "light.auto":
            auto_calls.append(service)

    seq.hass.services.async_call = mock_call

    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_shutdown()
    assert len(auto_calls) > 0


@pytest.mark.asyncio
async def test_phase_shutdown_cancelled(hass):
    seq = _make_seq()
    seq.hass = hass
    seq.lights = ["light.test"]
    seq._lights_data = {
        "light.test": {"capabilities": {"color_temp", "brightness"}},
    }
    seq._cancelled = True

    with patch("custom_components.adaptive_lighting.sunrise.asyncio.sleep", AsyncMock()):
        await seq._phase_shutdown()


@pytest.mark.asyncio
async def test_async_register_service(hass):
    SunriseSequence.async_register_service(hass)
    assert hass.services.has_service("adaptive_lighting", "sunrise")


def test_sunrise_schema_valid():
    assert SUNRISE_SCHEMA is not None
    schema_keys = list(SUNRISE_SCHEMA.schema.keys())
    assert "lights" in schema_keys
    assert "duration" in schema_keys
    assert "hold_time" in schema_keys


def _make_seq():
    ctx = Context(id="test-sunrise-ctx")
    hass = Mock(spec=HomeAssistant)
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
