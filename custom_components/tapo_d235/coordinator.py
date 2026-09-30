"""Data coordinator for a locally connected Tapo D235."""

from __future__ import annotations

import logging
from typing import Any

from kasa import Discover
from kasa.exceptions import KasaException

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class D235Coordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch a single D235 and retain its initialized python-kasa device."""

    def __init__(
        self,
        hass: HomeAssistant,
        *,
        host: str,
        username: str,
        password: str,
        stream_username: str | None,
        stream_password: str | None,
    ) -> None:
        """Initialize the D235 coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.host = host
        self.username = username
        self.password = password
        self.stream_username = stream_username or None
        self.stream_password = stream_password or None
        self.device: Any | None = None

    async def _async_update_data(self) -> dict[str, Any]:
        """Update the doorbell once and return its currently available features."""
        try:
            if self.device is None:
                self.device = await Discover.discover_single(
                    self.host,
                    username=self.username,
                    password=self.password,
                )
                if self.device is None:
                    raise UpdateFailed("No Tapo device responded at the configured address")
            await self.device.update()
        except (KasaException, OSError, TimeoutError) as err:
            raise UpdateFailed(f"Error communicating with D235: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected D235 update error: {err}") from err

        return {
            "alias": self.device.alias,
            "features": tuple(self.device.features),
            "model": getattr(self.device, "model", "D235"),
        }

