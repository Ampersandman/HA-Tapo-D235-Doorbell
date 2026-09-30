"""Direct connection helpers for the Tapo D235."""

from __future__ import annotations

from typing import Any

from kasa import Credentials, Device, DeviceConfig
from kasa.deviceconfig import (
    DeviceConnectionParameters,
    DeviceEncryptionType,
    DeviceFamily,
)


async def async_connect_d235(
    host: str, username: str, password: str
) -> Any:
    """Connect directly to a D235 without relying on UDP discovery.

    D235 doorbells use the SmartCam HTTPS transport. Providing these connection
    parameters is required when the device does not answer UDP discovery, which
    is common on Wi-Fi, VLAN, and multicast-restricted networks.
    """
    config = DeviceConfig(
        host=host,
        credentials=Credentials(username=username, password=password),
        connection_type=DeviceConnectionParameters(
            device_family=DeviceFamily.SmartTapoDoorbell,
            encryption_type=DeviceEncryptionType.Aes,
            https=True,
        ),
    )
    return await Device.connect(config=config)
