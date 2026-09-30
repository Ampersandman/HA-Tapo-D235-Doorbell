"""Number platform for D235 python-kasa features."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import D235Entity, feature_type


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create entities for every number feature reported by the D235."""
    coordinator = entry.runtime_data["coordinator"]
    async_add_entities(
        D235Number(coordinator, feature_id)
        for feature_id, feature in coordinator.device.features.items()
        if feature_type(feature) == "number"
    )


class D235Number(D235Entity, NumberEntity):
    """A numeric configurable python-kasa feature."""

    def __init__(self, coordinator, feature_id: str) -> None:
        """Initialize range metadata from python-kasa."""
        super().__init__(coordinator, feature_id)
        self._attr_native_min_value = self.feature.minimum_value
        self._attr_native_max_value = self.feature.maximum_value
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = self.feature.unit

    @property
    def native_value(self) -> float | None:
        """Return the latest library value."""
        value = self.feature.value
        return None if value is None else float(value)

    async def async_set_native_value(self, value: float) -> None:
        """Set the numeric value."""
        await self.async_set_feature_value(int(value) if value.is_integer() else value)

