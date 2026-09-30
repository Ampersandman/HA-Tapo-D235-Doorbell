"""Direct connection helpers for the Tapo D235."""

from __future__ import annotations

from typing import Any

from kasa import Credentials, Device, DeviceConfig
from kasa.deviceconfig import (
    DeviceConnectionParameters,
    DeviceEncryptionType,
    DeviceFamily,
)
from kasa.exceptions import KasaException


class TpapDependencyUnavailable(Exception):
    """Raised when Home Assistant still has the older python-kasa package."""


async def _async_connect_with_transport(
    host: str,
    username: str,
    password: str,
    encryption_type: DeviceEncryptionType,
) -> Any:
    """Connect to a D235 using one explicitly selected local transport."""
    config = DeviceConfig(
        host=host,
        credentials=Credentials(username=username, password=password),
        connection_type=DeviceConnectionParameters(
            device_family=DeviceFamily.SmartTapoDoorbell,
            encryption_type=encryption_type,
            https=True,
            # D235 camera control starts on the camera HTTPS endpoint. A TPAP
            # device can announce a different control port during its unauthenticated
            # discovery exchange, which python-kasa then adopts for the session.
            http_port=443,
        ),
    )
    return await Device.connect(config=config)


def _is_tpap_discovery_mismatch(error: KasaException) -> bool:
    """Return whether a D235 responded but did not advertise TPAP.

    Do not fall back after a TPAP authentication failure: a second login attempt
    using another protocol can extend a device-side login lockout. The TPAP
    transport performs an unauthenticated discovery request before it submits
    credentials, so only that explicit protocol mismatch is safe to fall back.
    """
    return "TPAP discover" in str(error)


async def async_connect_d235(
    host: str, username: str, password: str
) -> Any:
    """Connect directly to a D235 without relying on UDP discovery.

    Recent D235 firmware can use TPAP, which is negotiated over the camera HTTPS
    endpoint and cannot be reached by the older AES-only python-kasa branch.
    Try TPAP first. Only a confirmed TPAP discovery mismatch falls back to the
    original AES SmartCam transport; authentication errors are always returned
    unchanged to avoid amplifying the device's lockout protection.
    """
    tpap_encryption = getattr(DeviceEncryptionType, "Tpap", None)
    if tpap_encryption is None:
        raise TpapDependencyUnavailable

    try:
        return await _async_connect_with_transport(
            host, username, password, tpap_encryption
        )
    except KasaException as error:
        if not _is_tpap_discovery_mismatch(error):
            raise

    return await _async_connect_with_transport(
        host, username, password, DeviceEncryptionType.Aes
    )
