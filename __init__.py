import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .sensor import IsraelRailwaysSensor, async_setup_entry

_LOGGER = logging.getLogger(__name__)

DOMAIN = "israel_railways"

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN] = entry.data
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
