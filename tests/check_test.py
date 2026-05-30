import sys
async def test_switch_debug(hass):
    from homeassistant.components.adaptive_lighting.const import DOMAIN
    from homeassistant.config_entries import ConfigEntryState
    from homeassistant.components.adaptive_lighting.const import (
        CONF_NAME, _DOMAIN_SCHEMA, UNDO_UPDATE_LISTENER
    )
    from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
    from tests.common import MockConfigEntry
    import homeassistant.util.dt as dt_util
    import datetime

    DEFAULT_NAME = "test"
    extra_data = {
        "lights": [],
        "sunrise_time": datetime.time(6, 0),
        "sunset_time": datetime.time(18, 0),
        "initial_transition": 0,
        "transition": 0,
        "detect_non_ha_changes": True,
        "prefer_rgb_color": False,
        "min_color_temp": 2500,
    }
    entry = MockConfigEntry(domain=DOMAIN, data={"name": DEFAULT_NAME, **extra_data})
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    sys.stdout.write(f"\n=== DEBUG ===\n")
    sys.stdout.write(f"entry.state = {entry.state}\n")
    d = hass.data.get(DOMAIN, {})
    sys.stdout.write(f"hass.data[{DOMAIN}] keys: {list(d.keys())}\n")
    if entry.entry_id in d:
        e = d[entry.entry_id]
        sys.stdout.write(f"entry_id data type: {type(e).__name__}\n")
        sys.stdout.write(f"keys: {list(e.keys()) if isinstance(e, dict) else 'N/A'}\n")
    sys.stdout.write(f"SWITCH_DOMAIN = {SWITCH_DOMAIN!r}\n")
    assert entry.state is ConfigEntryState.LOADED
    switch = hass.data[DOMAIN][entry.entry_id][SWITCH_DOMAIN]
    sys.stdout.write(f"OK: switch = {switch}\n")
