import ujson as json
from machine import Pin
import utime as time
import network

import urequests as requests
from umqtt.simple import MQTTClient

from credenciales import ssid, password
from settings import *

led = Pin(2, Pin.OUT)

led.value(0)
print('\nConectandose a la wifi...', end='')
red = network.WLAN(network.STA_IF)
red.active(True)
red.connect(ssid, password)
while not red.isconnected():
    time.sleep(0.1)
print('conectado!')
print(red.ifconfig())
led.value(1)

def sub_cb(topic, msg):
    topic = topic.decode()
    msg = msg.decode()

    print('')
    print("Me llego por '{}' esto: '{}' ".format(topic, msg))
    if topic == 'proyectoEOI':
        if msg == '{“id”: 38350, “value”: 1}':
            if led.value() == 0:
                print('Se ha intentado encender la luz pero ya estaba encendida')
                return
            print('Encendiendo luz')
            led.value(0)
        elif msg == '{“id”: 38350, “value”: 0}':
            if led.value() is 1:
                print('Se ha intentado apagar la luz pero ya estaba apagada')
                return
            print('Apagando luz')
            led.value(1)


client = MQTTClient(ID, MQTT_SERVER)
client.connect()
client.set_callback(sub_cb)
client.subscribe(TOPIC)

print('Encendido, configuracion y conexion completadas')
while True:
    client.check_msg()
    time.sleep(5)
