import sys
from server.types.handler import Handler
from server.img_detection import getEmotion


def start_handler(handler: Handler):
    if handler.msg["topic"] == "auth/login":
        patient_id = handler.fingerprint.get_patient_id()
        data = handler.db.find_patient(patient_id=patient_id)
        exclude_keys = ["_id"]
        if data is None:
            print("No patient found, try again")
        else:
            print("Patient found")
            handler.patient_id = patient_id
            handler.user_data = {
                k: data[k]
                for k in set(list(data.keys())) - set(exclude_keys)
            }
            handler.mqtt.client.publish("fingerprint/name",
                                        handler.user_data["name"])
            handler.next()

    if handler.msg["topic"] == "auth/signup" and type(
            handler.msg["payload"]) is dict:
        handler.user_data = handler.msg["payload"]
        patient_id = handler.db.insert_patient(handler.user_data)
        handler.fingerprint.register_finger(id=patient_id)
        handler.patient_id = patient_id
        handler.mqtt.client.publish("fingerprint/name",
                                    handler.user_data["name"])
        handler.next()


def serial_handler(handler: Handler):
    sensors = ["height", "temp", "spo2", "hr"]
    for sensor in sensors:
        while True:
            data = handler.serial.read_serial()
            if type(data) == "dict" and (sensor in data):
                handler.sensor_data[sensor] = data[sensor]
                handler.mqtt.client.publish(sensor, data[sensor])
                break
    handler.next()


def height_handler(handler: Handler):
    if handler.msg["topic"] == "height":
        print("Recieved height")
        handler.sensor_data["heart"] = handler.msg["payload"]
        handler.next()


def temp_handler(handler: Handler):
    if handler.msg["topic"] == "temp":
        print("Recieved temp")
        handler.sensor_data["temp"] = handler.msg["payload"]
        handler.next()


def spo2_handler(handler: Handler):
    if handler.msg["topic"] == "spo2":
        print("Recieved spo2")
        handler.sensor_data["spo2"] = handler.msg["payload"]
        handler.next()


def hr_handler(handler: Handler):
    if handler.msg["topic"] == "hr":
        print("Recieved hr")
        handler.sensor_data["hr"] = handler.msg["payload"]
        handler.next()


def camera_handler(handler: Handler):
    emotion = getEmotion()
    handler.sensor_data["emotion_detect"] = emotion
    handler.next()


def end_handler(handler: Handler):
    handler.db.insert_record(data=handler.sensor_data,
                             patient_id=handler.patient_id)


def email_handler(handler: Handler):
    handler.mqtt.client.publish("data/sensor", "height")
