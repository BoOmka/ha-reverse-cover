"""Cover platform for Reverse Cover."""

from __future__ import annotations

from homeassistant.components.cover import (
    ATTR_CURRENT_POSITION,
    ATTR_POSITION,
    DOMAIN as COVER_DOMAIN,
    SERVICE_CLOSE_COVER,
    SERVICE_OPEN_COVER,
    SERVICE_SET_COVER_POSITION,
    SERVICE_STOP_COVER,
    CoverEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITY_ID, STATE_CLOSED, STATE_CLOSING, STATE_OPEN, STATE_OPENING
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_SOURCE_ENTITY_ID, DOMAIN

STATE_MAP = {
    STATE_OPEN: STATE_CLOSED,
    STATE_CLOSED: STATE_OPEN,
    STATE_OPENING: STATE_CLOSING,
    STATE_CLOSING: STATE_OPENING,
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Reverse Cover from a config entry."""
    async_add_entities([ReverseCoverEntity(hass, entry)])


class ReverseCoverEntity(CoverEntity):
    """Representation of a reversed cover."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self._source_entity_id = entry.data[CONF_SOURCE_ENTITY_ID]
        self._attr_unique_id = f"reverse_{self._source_entity_id}"
        self._attr_name = f"Reverse {self._source_entity_id}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._source_entity_id)},
            "name": f"Reverse {self._source_entity_id}",
        }

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        async_track_state_change_event(
            self.hass, [self._source_entity_id], self._handle_source_event
        )

    @callback
    def _handle_source_event(self, _event) -> None:
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        return self.hass.states.get(self._source_entity_id) is not None

    @property
    def current_cover_position(self) -> int | None:
        state = self.hass.states.get(self._source_entity_id)
        if not state:
            return None
        position = state.attributes.get(ATTR_CURRENT_POSITION)
        if position is None:
            return None
        return 100 - position

    @property
    def is_opening(self) -> bool | None:
        state = self.hass.states.get(self._source_entity_id)
        if not state:
            return None
        return state.state == STATE_CLOSING

    @property
    def is_closing(self) -> bool | None:
        state = self.hass.states.get(self._source_entity_id)
        if not state:
            return None
        return state.state == STATE_OPENING

    @property
    def state(self) -> str | None:
        source = self.hass.states.get(self._source_entity_id)
        if not source:
            return None
        return STATE_MAP.get(source.state, source.state)

    async def async_open_cover(self, **kwargs) -> None:
        """Open the cover."""
        await self.hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_CLOSE_COVER,
            {CONF_ENTITY_ID: self._source_entity_id},
            blocking=True,
        )

    async def async_close_cover(self, **kwargs) -> None:
        """Close the cover."""
        await self.hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_OPEN_COVER,
            {CONF_ENTITY_ID: self._source_entity_id},
            blocking=True,
        )

    async def async_stop_cover(self, **kwargs) -> None:
        """Stop the cover."""
        await self.hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_STOP_COVER,
            {CONF_ENTITY_ID: self._source_entity_id},
            blocking=True,
        )

    async def async_set_cover_position(self, **kwargs) -> None:
        """Set cover position."""
        position = kwargs.get(ATTR_POSITION)
        if position is None:
            return
        await self.hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_SET_COVER_POSITION,
            {
                CONF_ENTITY_ID: self._source_entity_id,
                ATTR_POSITION: 100 - position,
            },
            blocking=True,
        )
