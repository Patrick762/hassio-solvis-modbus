"""Constants for the Solvis Modbus integration."""

from dataclasses import dataclass
from enum import Flag
from typing import Final

DOMAIN = "solvis_modbus"
MANUFACTURER = "Solvis"

DATA_COORDINATOR = "coordinator"

CONF_HEATER_TYPE: Final = "heater_type"


class HeaterType(Flag):
    """Enum for heater types."""

    GAS_BOILER = 1
    HEAT_PUMP = 2


@dataclass(frozen=True)
class ModbusFieldConfig:
    name: str
    address: int
    unit: str
    device_class: str
    state_class: str
    multiplier: float = 0.1


PORT = 502
DEFAULT_REGISTERS = [
    ModbusFieldConfig(
        name="outdoor_air_temp",
        address=33033,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="roof_air_temp",
        address=33031,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="cold_water_temp",
        address=33034,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
        multiplier=0.01,
    ),
    ModbusFieldConfig(
        name="flow_water_temp",
        address=33035,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="domestic_water_temp",
        address=33025,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="solar_water_temp",
        address=33030,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="solar_heat_exchanger_in_water_temp",
        address=33029,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="solar_heat_exchanger_out_water_temp",
        address=33028,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="tank_layer1_water_temp",
        address=33026,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="tank_layer2_water_temp",
        address=33032,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="tank_layer3_water_temp",
        address=33027,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="tank_layer4_water_temp",
        address=33024,
        unit="°C",
        device_class="temperature",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="solar_water_flow",
        address=33040,
        unit="L/min",
        device_class="volume_flow_rate",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="domestic_water_flow",
        address=33041,
        unit="L/min",
        device_class="volume_flow_rate",
        state_class="measurement",
    ),
]


GAS_REGISTERS = [
    ModbusFieldConfig(
        name="gas_power",
        address=33539,
        unit="kW",
        device_class="power",
        state_class="measurement",
    ),
]

HEAT_PUMP_REGISTERS = [
    ModbusFieldConfig(
        name="heat_pump_thermal_power",
        address=33544,
        unit="kW",
        device_class="power",
        state_class="measurement",
    ),
    ModbusFieldConfig(
        name="heat_pump_electric_power",
        address=33545,
        unit="kW",
        device_class="power",
        state_class="measurement",
    ),
]


REGISTERS = [
    *DEFAULT_REGISTERS,
    *GAS_REGISTERS,
    *HEAT_PUMP_REGISTERS,
]
