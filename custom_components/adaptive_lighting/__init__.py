"""Adaptive Lighting integration in Home-Assistant."""

import dataclasses
import logging
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry, ConfigEntryNotReady
from homeassistant.const import CONF_SOURCE
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant

from .const import (
    _DOMAIN_SCHEMA,  # pyright: ignore[reportPrivateUsage]
    ATTR_ADAPTIVE_LIGHTING_MANAGER,
    CONF_NAME,
    DOMAIN,
    UNDO_UPDATE_LISTENER,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch"]


@dataclasses.dataclass
class AdaptiveLightingData:
    """Runtime data stored per config entry."""

    undo_update_listener: CALLBACK_TYPE
    sleep_mode_switch: Any = None
    adapt_color_switch: Any = None
    adapt_brightness_switch: Any = None
    switch: Any = None


def _all_unique_names(value: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate that all entities have a unique profile name."""
    hosts = [device[CONF_NAME] for device in value]
    schema = vol.Schema(vol.Unique())
    schema(hosts)
    return value


CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.All(cv.ensure_list, [_DOMAIN_SCHEMA], _all_unique_names)},
    extra=vol.ALLOW_EXTRA,
)


async def reload_configuration_yaml(event: Event) -> None:
    """Reload configuration.yaml."""
    hass: HomeAssistant | None = event.data.get("hass")
    if hass is not None:
        await hass.services.async_call("homeassistant", "check_config", {})
    else:
        _LOGGER.error("HomeAssistant instance not found in event data.")


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Import integration from config."""
    if DOMAIN in config:
        for entry in config[DOMAIN]:
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN,
                    context={CONF_SOURCE: SOURCE_IMPORT},
                    data=entry,
                ),
            )
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up the component."""
    try:
        data = hass.data.setdefault(DOMAIN, {})

        # This will reload any changes the user made to any YAML configurations.
        # Called during 'quick reload' or hass.reload_config_entry
        hass.bus.async_listen("hass.config.entry_updated", reload_configuration_yaml)

        undo_listener = config_entry.add_update_listener(async_update_options)
        runtime_data = AdaptiveLightingData(undo_update_listener=undo_listener)
        config_entry.runtime_data = runtime_data
        # Backward compat: also store in hass.data[DOMAIN][entry_id] for
        # _switches_with_lights and _switches_from_service_call lookups
        data[config_entry.entry_id] = {UNDO_UPDATE_LISTENER: undo_listener}
        await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    except Exception:
        _LOGGER.exception(
            "Error setting up Adaptive Lighting entry %s",
            config_entry.title,
        )
        raise ConfigEntryNotReady from None
    else:
        return True


async def async_update_options(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(
        config_entry,
        "switch",
    )
    data = hass.data[DOMAIN]
    data[config_entry.entry_id][UNDO_UPDATE_LISTENER]()
    if unload_ok:
        data.pop(config_entry.entry_id)

    if len(data) == 1 and ATTR_ADAPTIVE_LIGHTING_MANAGER in data:
        # no more config_entries
        manager = data.pop(ATTR_ADAPTIVE_LIGHTING_MANAGER)
        manager.disable()

    if not data:
        hass.data.pop(DOMAIN)

    return unload_ok
