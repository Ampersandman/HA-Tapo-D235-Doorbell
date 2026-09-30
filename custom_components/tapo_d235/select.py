"""Select platform for D235 python-kasa features."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import D235Entity, as_native, feature_type


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create entities for every choice feature reported by the D235."""
    coordinator = entry.runtime_data["coordinator"]
    async_add_entities(
        D235Select(coordinator, feature_id)
        for feature_id, feature in coordinator.device.features.items()
        if feature_type(feature) == "choice"
    )


class D235Select(D235Entity, SelectEntity):
    """A selected-choice python-kasa feature."""

    @property
    def options(self) -> list[str]:
        """Return choices reported by the doorbell."""
        return [str(option) for option in self.feature.choices or []]

    @property
    def current_option(self) -> str | None:
        """Return the current choice."""
        value = as_native(self.feature.value)
        return None if value is None else str(value)

    async def async_select_option(self, option: str) -> None:
        """Set the selected choice."""
        await self.async_set_feature_value(option)

