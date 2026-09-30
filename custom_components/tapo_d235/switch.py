"""Switch platform for D235 python-kasa features."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import D235Entity, feature_type


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create entities for every switch feature reported by the D235."""
    coordinator = entry.runtime_data["coordinator"]
    async_add_entities(
        D235Switch(coordinator, feature_id)
        for feature_id, feature in coordinator.device.features.items()
        if feature_type(feature) == "switch"
    )


class D235Switch(D235Entity, SwitchEntity):
    """A boolean, configurable python-kasa feature."""

    @property
    def is_on(self) -> bool:
        """Return the latest library value."""
        return bool(self.feature.value)

    async def async_turn_on(self, **kwargs: object) -> None:
        """Turn the library feature on."""
        await self.async_set_feature_value(True)

    async def async_turn_off(self, **kwargs: object) -> None:
        """Turn the library feature off."""
        await self.async_set_feature_value(False)

