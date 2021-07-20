from machine import Pin

pwr1 = Pin(25, Pin.OUT)
pwr2 = Pin(21, Pin.OUT)
pwr1.value(1)
pwr2.value(1)

import utime
import ustruct
from ulora import TTN, uLoRa
import ujson
import ubinascii

utime.sleep(1)

print('Opening secrets')
with open('secrets.json') as fp:
    secrets = ujson.loads(fp.read())

print('Setting params')
REGION = secrets['the things network']['region']
DEVICE_ADDRESS = bytearray(ubinascii.unhexlify(secrets['the things network']['device address']))
NETWORK_SESSION_KEY = bytearray(ubinascii.unhexlify(secrets['the things network']['network session key']))
APP_SESSION_KEY = bytearray(ubinascii.unhexlify(secrets['the things network']['app session key']))

LORA_CS = const(18)
LORA_SCK = const(5)
LORA_MOSI = const(27)
LORA_MISO = const(19)
LORA_IRQ = const(26)
LORA_RST = const(14)
LORA_DATARATE = "SF7BW125"

TTN_CONFIG = TTN(DEVICE_ADDRESS, NETWORK_SESSION_KEY, APP_SESSION_KEY, country=REGION)
FPORT = 1
lora = uLoRa(
    cs=LORA_CS,
    sck=LORA_SCK,
    mosi=LORA_MOSI,
    miso=LORA_MISO,
    irq=LORA_IRQ,
    rst=LORA_RST,
    ttn_config=TTN_CONFIG,
    datarate=LORA_DATARATE,
    fport=FPORT
)

epoch = utime.time()
payload = ustruct.pack('h', 1)

print('Sending payload')
lora.send_data(payload, len(payload), lora.frame_counter)

print('Waiting 10 seconds for message to send')
utime.sleep(10)

print('Going to sleep now')

while True:
    print("attempting to close power relay")
    pwr1.value(0)
    pwr2.value(0)
    print('Sleep failed')
    utime.sleep(10)
    # todo, add error message when door left open
