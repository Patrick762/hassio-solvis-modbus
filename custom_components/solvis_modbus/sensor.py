"""Solvis sensors."""

import logging
from decimal import Decimal

from homeassistant.components.sensor import SensorEntity, CONF_STATE_CLASS
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_DEVICE_CLASS,
    EntityCategory,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DATA_COORDINATOR, DOMAIN, MANUFACTURER, REGISTERS
from .coordinator import PollingCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Setup sensor entities."""

    device_name = entry.data.get(CONF_NAME)
    address = entry.data.get(CONF_IP_ADDRESS)
    if address is None:
        _LOGGER.error("Device has no address")

    # Generate device info
    _LOGGER.error("Creating sensors for device with address %s", address)
    device_info = DeviceInfo(
        identifiers={(DOMAIN, entry.data.get(CONF_IP_ADDRESS))},
        name=entry.title,
        manufacturer=MANUFACTURER,
        model="Solvis Control 3",
    )

    # Add sensors according to device_info

    ###########
    #########       TODO: Not creating entities!!!!
    ##########

    sensors_to_add = []

    for register in REGISTERS:
        sensors_to_add.append(
            SolvisSensor(
                hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR],
                device_info,
                address,
                register.name,
                register.unit,
                register.device_class,
                register.state_class,
            )
        )

    async_add_entities(sensors_to_add)

class SolvisSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: PollingCoordinator,
        device_info: DeviceInfo,
        address,
        name: str,
        unit_of_measurement: str | None = None,
        device_class: str | None = None,
        state_class: str | None = None,
    ):
        """Init entity."""
        super().__init__(coordinator)

        self._address = address
        self._response_key = name

        self._attr_device_info = device_info
        self._attr_available = False
        self._attr_native_unit_of_measurement = unit_of_measurement
        self._attr_device_class = device_class
        self._attr_state_class = state_class

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        
        if self.coordinator.data is None:
            _LOGGER.warning("Data from coordinator is None. Skipping update")
            return
        
        if not isinstance(self.coordinator.data, dict):
            _LOGGER.warning(
                "Invalid data from coordinator"
            )
            self._attr_available = False
            return
        
        response_data = self.coordinator.data.get(self._response_key)
        if response_data is None:
            _LOGGER.warning("No data for available for (%s)", self._response_key)
            self._attr_available = False
            return
        
        if (
            not isinstance(response_data, int)
            and not isinstance(response_data, float)
            and not isinstance(response_data, complex)
            and not isinstance(response_data, Decimal)
        ):
            _LOGGER.warning(
                "Invalid response data type from coordinator. %s has type %s",
                response_data,
                type(response_data),
            )
            self._attr_available = False
            return
        
        self._attr_available = True
        self._attr_native_value = response_data
        self.async_write_ha_state()
