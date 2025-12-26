Steps:
- uart hello world with ESP32 board
- connect to wifi and ping local machine
- send and receive to a server over network
- kick the tires on servo

Misc:
- `source /opt/esp-idf/export.sh`: must be run to put `idf.py` and other tools in the current path
- `idf.py set-target esp32s3`: set build target to esp32s3. Must be done at least
once in order to flash.
- `idf.py -p /dev/ttyACM0 -b 115200 flash`: flash the 
