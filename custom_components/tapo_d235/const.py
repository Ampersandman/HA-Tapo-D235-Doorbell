"""Constants for the Tapo D235 Doorbell integration."""

from datetime import timedelta
from typing import Final

DOMAIN: Final = "tapo_d235"
PLATFORMS: Final = (
    "binary_sensor",
    "button",
    "camera",
    "number",
    "select",
    "sensor",
    "switch",
)

CONF_STREAM_USERNAME: Final = "stream_username"
CONF_STREAM_PASSWORD: Final = "stream_password"
DEFAULT_SCAN_INTERVAL: Final = timedelta(seconds=30)

