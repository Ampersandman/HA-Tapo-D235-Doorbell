"""Sensor platform for read-only D235 python-kasa features."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import D235Entity, as_native, feature_type


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create entities for every sensor feature reported by the D235."""
    coordinator = entry.runtime_data["coordinator"]
    async_add_entities(
        D235Sensor(coordinator, feature_id)
        for feature_id, feature in coordinator.device.features.items()
        if feature_type(feature) == "sensor"
    )


class D235Sensor(D235Entity, SensorEntity):
    """A read-only python-kasa feature."""

    @property
    def native_value(self) -> Any:
        """Return the latest library value."""
        return as_native(self.feature.value)

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit reported by python-kasa, if any."""
        return self.feature.unit

