"""Adds config flow for Tibber integration."""
from __future__ import annotations

from typing import Any
from typing import Callable
import aiohttp
import tibber
import voluptuous as vol

from homeassistant.config_entries import *
from homeassistant.core import callback
from homeassistant.const import CONF_ACCESS_TOKEN

from homeassistant import data_entry_flow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import selector

from .const import DOMAIN

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_ACCESS_TOKEN): str
    })

ERR_TIMEOUT = "timeout"
ERR_CLIENT = "cannot_connect"
ERR_TOKEN = "invalid_access_token"
TOKEN_URL = "https://developer.tibber.com/settings/access-token"


class TibberConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tibber integration."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        # This is for backwards compatibility.
        return await self.async_step_init(user_input)


    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        #self._async_abort_entries_match()

        if user_input is not None:
            access_token = user_input[CONF_ACCESS_TOKEN].replace(" ", "")

            tibber_connection = tibber.Tibber(
                access_token=access_token,
                websession=async_get_clientsession(self.hass),
            )

            errors = {}

            try:
                await tibber_connection.update_info()
            except TimeoutError:
                errors[CONF_ACCESS_TOKEN] = ERR_TIMEOUT
            except tibber.InvalidLogin:
                errors[CONF_ACCESS_TOKEN] = ERR_TOKEN
            except (
                aiohttp.ClientError,
                tibber.RetryableHttpExceptionError,
                tibber.FatalHttpException,
            ):
                errors[CONF_ACCESS_TOKEN] = ERR_CLIENT

            if errors:
                return self.async_show_form(
                    step_id="user",
                    data_schema=DATA_SCHEMA,
                    description_placeholders={"url": TOKEN_URL},
                    errors=errors,
                )

            unique_id = tibber_connection.user_id
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=tibber_connection.name,
                data={CONF_ACCESS_TOKEN: access_token},
                options = {
                    "surcharge_price_excl" : 0.2,
                    "tax_rate":0,
                    "tax_per_kwh": 0.10
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            description_placeholders={"url": TOKEN_URL},
            errors={},
        )
 
    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(OptionsFlow):
    
    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        
        """Manage the options."""
        if user_input is not None:

            
            return self.async_create_entry(title="", 
                data=user_input,
                )

        return self.async_show_form(
            step_id="init",
            data_schema= vol.Schema({
                vol.Required("surcharge_price_excl", default=self.config_entry.options.get("surcharge_price_excl"),): float,

                vol.Required("tax_rate", default=self.config_entry.options.get("tax_rate")):  selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0,
                        max=100,
                        step=0.01,
                        mode=selector.NumberSelectorMode.BOX,
                    ),
                ),

                vol.Required("tax_per_kwh", default=self.config_entry.options.get("tax_per_kwh")):  selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0,
                        max=100,
                        mode=selector.NumberSelectorMode.BOX,
                    ),
                ),
            }),

        )