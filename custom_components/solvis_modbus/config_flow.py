"""Config flow for Solvis integration."""

import logging
import re
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SolvisConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Solvis Modbus devices."""

    def __init__(self) -> None:
        _LOGGER.info("Initialize config flow for %s", DOMAIN)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle user input."""

        if user_input is not None:
            address = user_input[CONF_IP_ADDRESS]
            name = user_input[CONF_NAME]
            await self.async_set_unique_id(address, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=re.sub("[^A-Za-z0-9_-]+", "", name),
                data={
                    CONF_IP_ADDRESS: address,
                    CONF_NAME: re.sub("[^A-Za-z0-9_-]+", "", name),
                },
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_IP_ADDRESS): str,
                vol.Required(CONF_NAME): str,
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )
