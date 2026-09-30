"""Shared entity support for dynamically reported python-kasa features."""

from __future__ import annotations

from enum import Enum
from typing import Any

from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import D235Coordinator


def feature_type(feature: Any) -> str:
    """Return a stable type name across supported python-kasa releases."""
    type_value = feature.type
    return getattr(type_value, "name", str(type_value)).lower()


def as_native(value: Any) -> Any:
    """Convert library values into Home Assistant-safe entity state values."""
    if isinstance(value, Enum):
        return value.value
    return value


class D235Entity(CoordinatorEntity[D235Coordinator]):
    """Base class for an entity backed by one python-kasa feature."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: D235Coordinator, feature_id: str) -> None:
        """Initialize a feature entity."""
        super().__init__(coordinator)
        self.feature_id = feature_id
        feature = self.feature
        self._attr_unique_id = f"{self.device_id}_{feature_id}"
        self._attr_name = feature.name
        self._attr_icon = feature.icon
        category = getattr(feature.category, "name", "").lower()
        if category == "config":
            self._attr_entity_category = EntityCategory.CONFIG
        elif category == "debug":
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def device(self) -> Any:
        """Return the initialized kasa device."""
        assert self.coordinator.device is not None
        return self.coordinator.device

    @property
    def device_id(self) -> str:
        """Return a stable device id, falling back to the configured host."""
        return str(getattr(self.device, "device_id", None) or self.coordinator.host)

    @property
    def feature(self) -> Any:
        """Return the live feature by id."""
        return self.device.features[self.feature_id]

    @property
    def device_info(self) -> DeviceInfo:
        """Describe the physical doorbell once for every exposed entity."""
        return DeviceInfo(
            identifiers={("tapo_d235", self.device_id)},
            name=self.coordinator.data.get("alias") or "Tapo D235 Doorbell",
            manufacturer="TP-Link",
            model=getattr(self.device, "model", None) or "Tapo D235",
            sw_version=getattr(self.device, "firmware", None),
        )

    @property
    def available(self) -> bool:
        """Report unavailable if the feature disappears after a device update."""
        return super().available and self.feature_id in self.device.features

    async def async_set_feature_value(self, value: Any = None) -> None:
        """Set a feature and request a coordinated refresh afterwards."""
        await self.feature.set_value(value)
        await self.coordinator.async_request_refresh()

