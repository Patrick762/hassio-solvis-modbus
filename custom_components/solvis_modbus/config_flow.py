"""Config flow for Solvis integration."""

import logging
import re
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult, FlowResult
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectOptionDict,
)

from .const import DOMAIN, HeaterType, CONF_HEATER_TYPE

_LOGGER = logging.getLogger(__name__)


class SolvisConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Solvis Modbus devices."""

    def __init__(self) -> None:
        _LOGGER.info("Initialize config flow for %s", DOMAIN)
        self._address: str | None = None
        self._name: str | None = None
        self._heater_type: list[str] | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle user input."""

        if user_input is not None:
            address = user_input[CONF_IP_ADDRESS]
            name = user_input[CONF_NAME]
            await self.async_set_unique_id(address, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            self._address = address
            self._name = name

            return await self.async_step_heater_type()

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

    async def async_step_heater_type(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Select Heater Type: Heat Pump, Gas Boiler"""
        assert self._address is not None
        assert self._name is not None

        if user_input is not None:
            self._heater_type = user_input["type"]
            assert self._heater_type is not None
            _LOGGER.info("Selected heater type: %s", self._heater_type)

            heater_type_compunt = HeaterType(0)
            for t in self._heater_type:
                heater_type_compunt |= HeaterType[t]

            return self.async_create_entry(
                title=re.sub("[^A-Za-z0-9_-]+", "", self._name),
                data={
                    CONF_IP_ADDRESS: self._address,
                    CONF_NAME: re.sub("[^A-Za-z0-9_-]+", "", self._name),
                },
                options={CONF_HEATER_TYPE: heater_type_compunt},
            )

        data_schema = vol.Schema(
            {
                vol.Required("type"): SelectSelector(
                    config=SelectSelectorConfig(
                        multiple=True,
                        translation_key=CONF_HEATER_TYPE,
                        options=[str(h_type.name) for h_type in HeaterType],
                    )
                )
            }
        )

        return self.async_show_form(
            step_id="heater_type",
            data_schema=data_schema,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "SolvisOptionsFlow":
        """Create the options flow."""
        return SolvisOptionsFlow(config_entry)


class SolvisOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle options."""
        if user_input is not None:
            heater_type_compunt = HeaterType(0)
            for t in user_input.get(CONF_HEATER_TYPE):
                heater_type_compunt |= HeaterType[t]
            return self.async_create_entry(data={CONF_HEATER_TYPE: heater_type_compunt})

        data_schema = vol.Schema(
            {
                vol.Required(CONF_HEATER_TYPE): SelectSelector(
                    config=SelectSelectorConfig(
                        multiple=True,
                        translation_key=CONF_HEATER_TYPE,
                        options=[
                            SelectOptionDict(
                                label=str(h_type.name), value=str(h_type.name)
                            )
                            for h_type in HeaterType
                        ],
                    )
                )
            }
        )

        data_schema = self.add_suggested_values_to_schema(
            data_schema,
            {
                CONF_HEATER_TYPE: [
                    h_type.name
                    for h_type in HeaterType
                    if h_type
                    & HeaterType(self.config_entry.options.get(CONF_HEATER_TYPE))
                ]
            },
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )
