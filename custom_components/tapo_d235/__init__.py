"""Tapo D235 Doorbell integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    CONF_DEVICE_ID,
    CONF_STREAM_PASSWORD,
    CONF_STREAM_USERNAME,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import D235Coordinator

type D235ConfigEntry = ConfigEntry[dict[str, D235Coordinator]]


async def async_setup_entry(hass: HomeAssistant, entry: D235ConfigEntry) -> bool:
    """Set up a D235 doorbell from a config entry."""
    coordinator = D235Coordinator(
        hass,
        host=entry.data[CONF_HOST],
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        stream_username=entry.options.get(CONF_STREAM_USERNAME),
        stream_password=entry.options.get(CONF_STREAM_PASSWORD),
        expected_device_id=entry.data.get(CONF_DEVICE_ID),
    )
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(f"Unable to connect to the D235 at {entry.data[CONF_HOST]}") from err

    entry.runtime_data = {"coordinator": coordinator}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: D235ConfigEntry) -> bool:
    """Unload a D235 config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok and (device := entry.runtime_data["coordinator"].device) is not None:
        await device.protocol.close()
    return unload_ok

