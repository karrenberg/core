"""Support for Vallox ventilation unit selects."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable # required?

from vallox_websocket_api import Vallox # required?

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    VALLOX_PROFILE_TO_PRESET_MODE,
    PRESET_MODE_TO_VALLOX_PROFILE,
    VALLOX_SUPPLY_HEATING_ADJUST_MODE_TO_STR,
    VALLOX_SUPPLY_HEATING_ADJUST_MODE_FROM_STR,
    VALLOX_DEFROST_MODE_TO_STR,
    VALLOX_DEFROST_MODE_FROM_STR,
)
from .coordinator import ValloxDataUpdateCoordinator
from .entity import ValloxEntity

class ValloxSelectEntity(ValloxEntity, SelectEntity):
    """Representation of a Vallox select."""

    entity_description: ValloxSelectEntityDescription
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        name: str,
        coordinator: ValloxDataUpdateCoordinator,
        description: ValloxSelectEntityDescription,
        client: Vallox,
    ) -> None:
        """Initialize the select."""
        super().__init__(name, coordinator)

        self.entity_description = description
        self._attr_options = list(description.values_to_str.values())
        self._attr_unique_id = f"{self._device_uuid}-{description.key}"
        self._client = client

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        mode = getattr(self.coordinator.data, self.entity_description.property_name)
        if mode is None:
            return None
        return self.entity_description.values_to_str[mode]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        try:
            value = self.entity_description.values_from_str[option]
        except KeyError as err:
            raise ValueError(f"Invalid option: {option}. Must be one of {self._attr_options}") from err
        await self.entity_description.set_method(self._client, value)
        await self.coordinator.async_request_refresh()


@dataclass(frozen=True, kw_only=True)
class ValloxSelectEntityDescription(SelectEntityDescription):
    """Describes Vallox select entity."""

    values_to_str: dict[int, str]
    values_from_str: dict[str, int]
    property_name: str
    set_method: Callable[[Vallox, int], Any]


SELECT_ENTITIES: tuple[ValloxSelectEntityDescription, ...] = (
    ValloxSelectEntityDescription(
        key="profile",
        translation_key="profile",
        values_to_str=VALLOX_PROFILE_TO_PRESET_MODE,
        values_from_str=PRESET_MODE_TO_VALLOX_PROFILE,
        property_name="profile",
        set_method=lambda client, value: client.set_profile(value),
    ),
    ValloxSelectEntityDescription(
        key="supply_heating_adjust_mode",
        translation_key="supply_heating_adjust_mode",
        values_to_str=VALLOX_SUPPLY_HEATING_ADJUST_MODE_TO_STR,
        values_from_str=VALLOX_SUPPLY_HEATING_ADJUST_MODE_FROM_STR,
        property_name="supply_heating_adjust_mode",
        set_method=lambda client, value: client.set_supply_heating_adjust_mode(value),
    ),
    ValloxSelectEntityDescription(
        key="defrost_mode",
        translation_key="defrost_mode",
        values_to_str=VALLOX_DEFROST_MODE_TO_STR,
        values_from_str=VALLOX_DEFROST_MODE_FROM_STR,
        property_name="defrost_mode",
        set_method=lambda client, value: client.set_defrost_mode(value),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the selects."""
    data = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        ValloxSelectEntity(
            data["name"], data["coordinator"], description, data["client"]
        )
        for description in SELECT_ENTITIES
    )
