"""Support for Vallox ventilation unit numbers."""

from __future__ import annotations

from dataclasses import dataclass

from vallox_websocket_api import Vallox

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    EntityCategory,
    UnitOfTemperature,
    UnitOfTime,
    PERCENTAGE,
    CONCENTRATION_PARTS_PER_MILLION
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    METRIC_KEY_PROFILE_FAN_SPEED_HOME,
    METRIC_KEY_PROFILE_FAN_SPEED_AWAY,
    METRIC_KEY_PROFILE_FAN_SPEED_BOOST,
)
from .coordinator import ValloxDataUpdateCoordinator
from .entity import ValloxEntity


class ValloxNumberEntity(ValloxEntity, NumberEntity):
    """Representation of a Vallox number entity."""

    entity_description: ValloxNumberEntityDescription
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        name: str,
        coordinator: ValloxDataUpdateCoordinator,
        description: ValloxNumberEntityDescription,
        client: Vallox,
    ) -> None:
        """Initialize the Vallox number entity."""
        super().__init__(name, coordinator)

        self.entity_description = description

        self._attr_unique_id = f"{self._device_uuid}-{description.key}"
        self._client = client

    @property
    def native_value(self) -> float | None:
        """Return the value reported by the sensor."""
        if (
            value := self.coordinator.data.get(self.entity_description.metric_key)
        ) is None:
            return None

        return float(value)

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self._client.set_values(
            {self.entity_description.metric_key: float(value)}
        )
        await self.coordinator.async_request_refresh()


@dataclass(frozen=True, kw_only=True)
class ValloxNumberEntityDescription(NumberEntityDescription):
    """Describes Vallox number entity."""

    metric_key: str


NUMBER_ENTITIES: tuple[ValloxNumberEntityDescription, ...] = (
    ValloxNumberEntityDescription(
        key="supply_air_target_home",
        translation_key="supply_air_target_home",
        metric_key="A_CYC_HOME_AIR_TEMP_TARGET",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=5.0,
        native_max_value=25.0,
        native_step=1.0,
    ),
    ValloxNumberEntityDescription(
        key="supply_air_target_away",
        translation_key="supply_air_target_away",
        metric_key="A_CYC_AWAY_AIR_TEMP_TARGET",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=5.0,
        native_max_value=25.0,
        native_step=1.0,
    ),
    ValloxNumberEntityDescription(
        key="supply_air_target_boost",
        translation_key="supply_air_target_boost",
        metric_key="A_CYC_BOOST_AIR_TEMP_TARGET",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=5.0,
        native_max_value=25.0,
        native_step=1.0,
    ),
    ValloxNumberEntityDescription(
        key="fan_speed_home",
        translation_key="fan_speed_home",
        metric_key=METRIC_KEY_PROFILE_FAN_SPEED_HOME,
        device_class=NumberDeviceClass.SPEED,
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=1.0,
    ),
    ValloxNumberEntityDescription(
        key="fan_speed_away",
        translation_key="fan_speed_away",
        metric_key=METRIC_KEY_PROFILE_FAN_SPEED_AWAY,
        device_class=NumberDeviceClass.SPEED,
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=1.0,
    ),
    ValloxNumberEntityDescription(
        key="fan_speed_boost",
        translation_key="fan_speed_boost",
        metric_key=METRIC_KEY_PROFILE_FAN_SPEED_BOOST,
        device_class=NumberDeviceClass.SPEED,
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=1.0,
    ),
    # TODO: If the duration is set, the profile is enabled automatically but the
    #       "default" duration remains the same. The intention of this was to
    #       a) allow updating the duration (increase/decrease remaining time of
    #       the active profile) and b) set the default duration.
    #       Apparently b) requires a different metric key.
    ValloxNumberEntityDescription(
        key="profile_duration_boost",
        translation_key="profile_duration_boost",
        metric_key="A_CYC_BOOST_TIMER",
        device_class=NumberDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        native_min_value=1.0,
        native_max_value=65535.0,
        native_step=1.0,
    ),
    ValloxNumberEntityDescription(
        key="profile_duration_fireplace",
        translation_key="profile_duration_fireplace",
        metric_key="A_CYC_FIREPLACE_TIMER",
        device_class=NumberDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        native_min_value=1.0,
        native_max_value=65535.0,
        native_step=1.0,
    ),
    ValloxNumberEntityDescription(
        key="profile_duration_extra",
        translation_key="profile_duration_extra",
        metric_key="A_CYC_EXTRA_TIMER",
        device_class=NumberDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        native_min_value=1.0,
        native_max_value=65535.0,
        native_step=1.0,
    ),
    ValloxNumberEntityDescription(
        key="co2_limit",
        translation_key="co2_limit",
        metric_key="A_CYC_CO2_THRESHOLD",
        device_class=NumberDeviceClass.CO2,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        native_min_value=500,
        native_max_value=2000,
        native_step=100,
        entity_registry_enabled_default=False,
    ),
    ValloxNumberEntityDescription(
        key="rh_basic_level",
        translation_key="rh_basic_level",
        metric_key="A_CYC_RH_BASIC_LEVEL",
        device_class=NumberDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=1.0,
        entity_registry_enabled_default=False,
    ),
    ValloxNumberEntityDescription(
        key="post_heater_winter_setpoint",
        translation_key="post_heater_winter_setpoint",
        metric_key="A_CYC_POST_HEATER_WINTER_SETPOINT",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=0.0,
        native_max_value=19.0,
        native_step=1.0,
        entity_registry_enabled_default=False,
    ),
    ValloxNumberEntityDescription(
        key="supply_air_defrost_temp",
        translation_key="supply_air_defrost_temp",
        metric_key="A_CYC_SUPPLY_AIR_DEFROST_TEMP",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=12.0,
        native_max_value=20.0,
        native_step=1.0,
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensors."""
    data = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        ValloxNumberEntity(
            data["name"], data["coordinator"], description, data["client"]
        )
        for description in NUMBER_ENTITIES
    )
