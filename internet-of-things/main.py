import utime as time
from machine import Pin
import network
import ujson as json

from umqtt.simple import MQTTClient

from credenciales import ssid, password
from settings import *


class Controller:
    def __init__(self):
        self.led = Pin(2, Pin.OUT)
        self.connect_wifi()
        self.mqtt_config()
        self.run()

    def connect_wifi(self):
        """ Using credentials on credenciales.py """
        self.led.value(0)
        print("\nConnecting to wifi...", end="")
        red = network.WLAN(network.STA_IF)
        red.active(True)
        red.connect(ssid, password)
        while not red.isconnected():
            time.sleep(0.1)
        print("Connected!")
        print(red.ifconfig())
        self.led.value(1)

    def mqtt_config(self):
        """ Simple MQTT config """
        self.client = MQTTClient(ID, MQTT_SERVER)
        self.client.connect()
        self.client.set_callback(self.sub_cb)
        self.client.subscribe(TOPIC)

    def run(self):
        print("Power on, setup and connection complete")
        print("Listening on topic: {}".format(TOPIC.decode()))
        while True:
            self.client.check_msg()
            time.sleep(5)

    def sub_cb(self, topic, msg):
        """ Callback for MQTT suscribed topics """
        topic = topic.decode()
        msg = msg.decode().lower()  # we're case insensitive!

        msg_dict = self.load_string_to_json(msg)

        print("")
        print("I got from '{}' this: '{}' ".format(topic, msg))

        try:
            if topic == TOPIC.decode():
                if msg_dict["id"] != int(ID):
                    print("Incorrect ID")
                    return

                if msg_dict["value"] == 1:  # turn on order
                    if self.check_if_light_is_already_on():
                        return
                    print("Turning ON the light")
                    self.led.value(0)

                elif msg_dict["value"] == 0:  # turn off order
                    if self.check_if_light_is_already_off():
                        return
                    print("Turning OFF the light")
                    self.led.value(1)
        except:
            error_text = 'The message cannot be parsed. Please, use a json with "id" and "value" keys'
            print(error_text)

    def check_if_light_is_already_on(self):
        if self.led.value() == 0:
            print("An attempt was made to turn on the light but it was already on")
            return True
        return False

    def check_if_light_is_already_off(self):
        if self.led.value() == 1:
            print("An attempt was made to turn off the light but it was already off")
            return True
        return False

    @staticmethod
    def load_string_to_json(string):
        try:
            loaded_json = json.loads(string)
        except:
            print("Error loading message. Is not a json.")
            return
        return loaded_json


controller = Controller()
