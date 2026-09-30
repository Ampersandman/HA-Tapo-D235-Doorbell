"""Binary-sensor platform for D235 python-kasa features."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import D235Entity, feature_type


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create entities for every binary-sensor feature reported by the D235."""
    coordinator = entry.runtime_data["coordinator"]
    async_add_entities(
        D235BinarySensor(coordinator, feature_id)
        for feature_id, feature in coordinator.device.features.items()
        if feature_type(feature) == "binarysensor"
    )


class D235BinarySensor(D235Entity, BinarySensorEntity):
    """A boolean read-only python-kasa feature."""

    @property
    def is_on(self) -> bool | None:
        """Return the latest library value."""
        value = self.feature.value
        return None if value is None else bool(value)

