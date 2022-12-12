from paho.mqtt import client


class MQTT:
    def __init__(self):
        self._subscribe_topics = ["data/user", "data/sensor", "auth"]
        self._host_name = "localhost"
        self._port = 1883
        self.client = client.Client()

    def start(self, on_connect, on_message, on_publish, on_subscribe):
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_publish = on_publish
        self.client.on_subscribe = on_subscribe
        self.client.connect(self._host_name, self._port)
        self.client.subscribe([(topic, 0) for topic in self._subscribe_topics])
        self.client.loop_start()
