# coffeeFreshOMeter

## Setup your device and listen for data_out events
1. Set your IoT Connector id in the file: `connector_id.txt`
2. Set your device ID in the file: `device_id.txt`
3. Provision Device: `python3 provision.py`
4. Set Config_IO: `python3 setConfigIO.py`
5. Listen for device_control events: `python3 subscribe.py`