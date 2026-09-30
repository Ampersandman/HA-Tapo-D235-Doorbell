"""Button platform for D235 python-kasa action features."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import D235Entity, feature_type


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create entities for every action feature reported by the D235."""
    coordinator = entry.runtime_data["coordinator"]
    async_add_entities(
        D235Button(coordinator, feature_id)
        for feature_id, feature in coordinator.device.features.items()
        if feature_type(feature) == "action"
    )


class D235Button(D235Entity, ButtonEntity):
    """An action-style python-kasa feature."""

    async def async_press(self) -> None:
        """Run the action exposed by python-kasa."""
        await self.async_set_feature_value()

