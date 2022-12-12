from server.types.handler import Handler


def start_handler(handler: Handler):
    if handler.msg["topic"] == "auth":
        if handler.msg["payload"] == "login":
            handler.next(1)

        if handler.msg["payload"] == "signup":
            handler.next(2)


def login_handler(handler: Handler):
    patient_id = "1"  # simulate getting fingerprint
    data = handler.db.find_patient(patient_id=patient_id)
    if data is None:
        print("No patient found, trying again")
    else:
        print("Patient found")
        handler.patient_id = patient_id
        handler.next(3)


def signup_handler(handler: Handler):
    if handler.msg["topic"] == "data/user" and type(
            handler.msg["payload"]) == "dict":
        patient_id = handler.db.insert_patient(handler.msg["payload"])
        handler.patient_id = patient_id
        handler.next(3)
    else:
        patient_id = "1"  # simulate getting fingerprint
        handler.mqtt.client.publish("fingerprint", patient_id)
        pass


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


def camera_handler(handler: Handler):
    handler.mqtt.client.publish("data/sensor", "height")


def end_handler(handler: Handler):
    handler.db.insert_record(data=handler.sensor_data,
                             patient_id=handler.patient_id)


def email_handler(handler: Handler):
    handler.mqtt.client.publish("data/sensor", "height")
