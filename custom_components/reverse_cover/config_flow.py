"""Config flow for Reverse Cover."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector

from .const import CONF_SOURCE_ENTITY_ID, DOMAIN


def _build_schema(hass: HomeAssistant) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_ENTITY_ID): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="cover")
            )
        }
    )


class ReverseCoverConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Reverse Cover."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            source_entity_id = user_input[CONF_ENTITY_ID]
            await self.async_set_unique_id(source_entity_id)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Reverse {source_entity_id}",
                data={CONF_SOURCE_ENTITY_ID: source_entity_id},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema(self.hass),
            errors=errors,
        )
