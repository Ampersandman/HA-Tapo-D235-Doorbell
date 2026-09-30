"""RTSP camera platform for the Tapo D235."""

from __future__ import annotations

from typing import Any

from kasa import Credentials, Module

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import D235Entity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Add the local RTSP camera when the D235 reports camera capability."""
    coordinator = entry.runtime_data["coordinator"]
    if coordinator.device.modules.get(Module.Camera):
        async_add_entities([D235Camera(coordinator)])


class D235Camera(D235Entity, Camera):
    """D235 live camera using the RTSP URL provided by python-kasa."""

    _attr_name = "Camera"
    _attr_supported_features = CameraEntityFeature.STREAM
    _attr_use_stream_for_stills = True

    @property
    def is_on(self) -> bool:
        """Return whether the camera is not in privacy mode."""
        return bool(self.feature.value)

    def __init__(self, coordinator) -> None:
        """Initialize the camera entity without a synthetic feature."""
        D235Entity.__init__(self, coordinator, "state")
        Camera.__init__(self)
        self._attr_unique_id = f"{self.device_id}_camera"
        self._attr_name = "Camera"

    async def stream_source(self) -> str | None:
        """Return the local RTSP source for Home Assistant's stream component."""
        camera: Any = self.device.modules.get(Module.Camera)
        credentials = None
        if self.coordinator.stream_username and self.coordinator.stream_password:
            credentials = Credentials(
                self.coordinator.stream_username, self.coordinator.stream_password
            )
        return camera.stream_rtsp_url(credentials)

