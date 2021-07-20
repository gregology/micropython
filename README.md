# MicroPython projects

note: my TTY is `/dev/tty.usbserial-0001`, on Mac you can find yours with `ls /dev/tty.*`.

## Erase & Flash ESP board

Use [esptool](https://github.com/espressif/esptool) to erase and flash the ESP32.

`esptool.py -p /dev/tty.usbserial-0001 -c esp32 -b 115200 erase_flash`

`esptool.py -c esp32 -p /dev/tty.usbserial-0001 -b 115200 write_flash -z 0x1000 esp32spiram-idf4-20210202-v1.14.bin`

[Download latest version of MicroPython](https://micropython.org/download/esp32/)

## Letterbox

Create a `letterbox/secrets.json` using `letterbox/secrets.json.example` as a template.

Refer to [device pinout / schematics diagrams for pin details](https://www.thethingsnetwork.org/forum/t/big-esp32-sx127x-topic-part-3/18436) and update these settings in `main.py`.

```
LORA_CS = const(18)
LORA_SCK = const(5)
LORA_MOSI = const(27)
LORA_MISO = const(19)
LORA_IRQ = const(26)
LORA_RST = const(14)
LORA_DATARATE = "SF7BW125"
```

Transfer files using [adafruit-ampy](https://pypi.org/project/adafruit-ampy/).

```
ampy -p /dev/tty.usbserial-0001 put letterbox/boot.py
ampy -p /dev/tty.usbserial-0001 put letterbox/main.py
ampy -p /dev/tty.usbserial-0001 put letterbox/ulora.py
ampy -p /dev/tty.usbserial-0001 put letterbox/ulora_encryption.py
ampy -p /dev/tty.usbserial-0001 put letterbox/ttn
ampy -p /dev/tty.usbserial-0001 put letterbox/secrets.json
```

## Watch output

`screen /dev/tty.usbserial-0001 115200`

## Decode payload in The Things Network Console

```
function Decoder(bytes, port) {
  // Decode an uplink message from a buffer
  // (array) of bytes to an object of fields.
  var decoded = {};

  // Decode bytes to int
  var testShort = (bytes[1] << 8) | bytes[0];

  // Decode int 
  decoded.short = testShort;

  return decoded;
}
```

[Credits](https://core-electronics.com.au/tutorials/encoding-and-decoding-payloads-on-the-things-network.html)

## Bridge The Things Network to local MQTT broker

Add to Mosquitto mosquitto.conf

```
# Bridge to The Things Network
connection bridge-ttn
address us-west.thethings.network:8883
remote_username APP_ID
remote_password ACCESS_KEYS
bridge_cafile /mosquitto/config/certs/ttn-ca.pem
bridge_insecure false
topic # both 0 ttn/ massassauga/devices/
```

[ttn-ca.pem](https://console.thethingsnetwork.org/mqtt-ca.pem) - [Credits](https://koen.vervloesem.eu/blog/bridge-the-things-network-to-your-local-mqtt-broker/)

## Add Home Assistant binary sensor

Add to Home Assistant configuration.yaml

```
 - platform: mqtt
   unique_id: 01234567-89ab-cdef-0123-456789abcdef
   name: "Letterbox Sensor"
   state_topic: "ttn/letterbox/up"
   value_template: "{{ value_json['payload_fields']['short'] }}"
   payload_on: 1
   payload_off: 0
   off_delay: 10
   icon: "mdi:mailbox"
   force_update: true
```

## Credits

 * [ESP32 LoRa TTN micropython example](https://gist.github.com/JoooostB/3ec62aaba6282660b9f8dd2e01cf24e5) by [JoooostB](https://gist.github.com/JoooostB)
 * [MicroPython: ESP32 Deep Sleep and Wake Up Sources](https://randomnerdtutorials.com/micropython-esp32-deep-sleep-wake-up-sources/)
