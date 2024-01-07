"""Coordinator for Solvis integration."""

import asyncio
from datetime import timedelta
import logging
import async_timeout
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder, Endian

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .const import REGISTERS

_LOGGER = logging.getLogger(__name__)

class PollingCoordinator(DataUpdateCoordinator):
    """Polling coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
    ):
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Solvis polling coordinator",
            update_interval=timedelta(seconds=20),
        )

        self._address = address

        # Create client
        self.logger.debug("Creating client")
        self.client = ModbusTcpClient(address)

        # polling mutex
        self.polling_lock = asyncio.Lock()

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """

        self.logger.debug("Polling data")

        parsed_data: dict = {}

        async with self.polling_lock:
            try:
                async with async_timeout.timeout(5):

                    # Connect to device
                    max_retries = 5
                    for attempt in range(1, max_retries + 1):
                        if not self.client.connected:

                            if attempt == max_retries:
                                raise ConnectionError()

                            self.client.connect()
                        else:
                            break
                    
                    # Read registers
                    for register in REGISTERS:
                        result = self.client.read_input_registers(
                            address=register.address,
                            slave=1,
                        )

                        # Add data to return values
                        if(len(result.registers) == 1):
                            d = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.BIG)
                            parsed_data[register.name] = round(d.decode_16bit_int() * register.multiplier, 2)

            except TimeoutError:
                self.logger.warning("Polling timed out")
            except ConnectionError:
                self.logger.warning("Couldn't connect to device")
            finally:
                self.client.close()

        # Pass data back to sensors
        return parsed_data
