"""Config flow for the Tapo D235 Doorbell integration."""

from __future__ import annotations

import voluptuous as vol
from kasa import Discover
from kasa.exceptions import KasaException

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_STREAM_PASSWORD, CONF_STREAM_USERNAME, DOMAIN


async def _validate_input(hass: HomeAssistant, data: dict[str, str]) -> dict[str, str]:
    """Verify credentials and ensure the selected host identifies as a D235."""
    device = await Discover.discover_single(
        data[CONF_HOST],
        username=data[CONF_USERNAME],
        password=data[CONF_PASSWORD],
    )
    if device is None:
        raise CannotConnect
    await device.update()
    model = str(getattr(device, "model", ""))
    if "D235" not in model.upper():
        raise UnsupportedDevice
    return {"title": device.alias or "Tapo D235 Doorbell"}


class TapoD235ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for a single local D235 doorbell."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial setup step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await _validate_input(self.hass, user_input)
            except (KasaException, OSError, TimeoutError):
                errors["base"] = "cannot_connect"
            except UnsupportedDevice:
                errors["base"] = "unsupported_device"
            except Exception:
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Return the options flow for separate RTSP credentials."""
        return TapoD235OptionsFlow()


class TapoD235OptionsFlow(OptionsFlow):
    """Allow setting a separate Camera Account for RTSP."""

    async def async_step_init(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Manage RTSP credentials."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_STREAM_USERNAME,
                        default=self.config_entry.options.get(CONF_STREAM_USERNAME, ""),
                    ): str,
                    vol.Optional(
                        CONF_STREAM_PASSWORD,
                        default=self.config_entry.options.get(CONF_STREAM_PASSWORD, ""),
                    ): str,
                }
            ),
        )


class CannotConnect(Exception):
    """The doorbell could not be reached."""


class UnsupportedDevice(Exception):
    """The configured host is not a D235."""

