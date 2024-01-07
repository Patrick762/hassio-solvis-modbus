# hassio-solvis-modbus
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Validate with hassfest](https://github.com/Patrick762/hassio-solvis-modbus/actions/workflows/hassfest_validation.yml/badge.svg)](https://github.com/Patrick762/hassio-solvis-modbus/actions/workflows/hassfest_validation.yml)
[![HACS Action](https://github.com/Patrick762/hassio-solvis-modbus/actions/workflows/HACS.yml/badge.svg)](https://github.com/Patrick762/hassio-solvis-modbus/actions/workflows/HACS.yml)

Home Assistant Integration for Solvis SC3

## Disclaimer
This integration is provided without any warranty or support by Solvis. I do not take responsibility for any problems it may cause in all cases. Use it at your own risk.

## Installation
To install this integration, you first need [HACS](https://hacs.xyz/) installed.
After the installation, you need to add the repository URL in HACS as custom repository: https://github.com/Patrick762/hassio-solvis-modbus
You can then search for "Solvis Modbus" in the HACS integrations.

## Adding devices
You can add devices via the home assistant integrations page by using the device ip address and setting a name. Sensors will then be added automatically.

### Available sensors

- Gas burner power
- Outdoor air temperature
- Outdoor air temperature on your roof (if using solar)
- Cold water temperature
- Flow water temperature
- Domestic water temperature
- Solar fluid temperature (if using solar)
- Solar heat exchanger input and output temperature (if using solar)
- Temperatures of the different layers in the water tank
- Flow rate of solar fluid and domestic water
