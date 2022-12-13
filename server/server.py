import ast
from queue import Queue

from typing import Dict, Callable

from server.database import Database
from server.handlers import *

from server.mqtt import MQTT
from server.serial import STM32Serial
from server.fingerprint import Fingerprint
from server.types.handler import Handler
from server.types.message import Message


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


class Server:

    def __init__(self):
        self.user_data = {}
        self.sensor_data = {}
        self.state_handlers: Dict[int, Callable[[Handler], None]] = {
            0: start_handler,
            1: height_handler,
            2: temp_handler,
            3: spo2_handler,
            4: hr_handler,
            5: camera_handler,
            6: end_handler,
        }
        self.state = 0
        self.patient_id = None
        self.mqtt = MQTT()
        self.queue = Queue()
        self.db = Database()
        self.fingerprint = Fingerprint()
        # self.serial = STM32Serial(port="/dev/bus/usb/001/004")

    def next_state(self, state: int = None):
        self.state = state if state else self.state + 1

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload.decode("utf-8")))
        try:
            payload = ast.literal_eval(str(msg.payload.decode("utf-8")))
        except Exception as e:
            payload = str(msg.payload.decode("utf-8"))
            print(e)
        print(type(payload))
        self.queue.put({"topic": msg.topic, "payload": payload})

    def start(self):
        self.mqtt.start(on_connect, self.on_message, on_publish, on_subscribe)
        while True:
            try:
                msg = self.queue.get(block=False)
            except Exception as e:
                msg: Message = {"payload": None, "topic": None}
            if self.state == 7:
                print("Done, terminating")
                break
            handler = Handler(mqtt=self.mqtt,
                              serial=None,
                              msg=msg,
                              next=self.next_state,
                              sensor_data=self.sensor_data,
                              user_data=self.user_data,
                              db=self.db,
                              patient_id=self.patient_id,
                              fingerprint=self.fingerprint)
            self.state_handlers[self.state](handler)
