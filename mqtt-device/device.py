import json
import os
import logging
from dataclasses import dataclass
from time import sleep

import paho.mqtt.client as mqtt


STATE = "off"
TEMP = 24
RPM = 1000
COLOR_TEMP = 3200


logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]%(message)s", level=logging.DEBUG)


@dataclass
class Config():
    broker_address: str
    name: str
    extra_param: str

    @classmethod
    def from_json_file(cls, path):
        with open(path) as f:
            config = json.load(f)

        return cls(
            config["broker_address"],
            config["name"],
            config["extra_param"],
            )

    @property
    def topic_base(self):
        return f"home/{self.name}"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to broker with result code {str(rc)}")
    # Subscribe to on/off topic
    client.subscribe(f"{userdata.topic_base}/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    decoded_payload = msg.payload.decode()
    token = msg.topic.split("/")[-1]
    logger.info(f"Received message on topic {msg.topic}: {decoded_payload}")
    if token == "state":
        handle_on_off(decoded_payload)
    elif token == "temp":
        handle_temp(decoded_payload)
    elif token == "rpm":
        handle_rpm(decoded_payload)
    elif token == "ct":
        handle_ct(decoded_payload)


def handle_temp(payload):
    global TEMP
    TEMP = int(payload)


def handle_rpm(payload):
    global RPM
    RPM = int(payload)


def handle_ct(payload):
    global COLOR_TEMP
    COLOR_TEMP = int(payload)


def handle_on_off(payload):
    global STATE
    if payload == "on":
        STATE = "on"
    elif payload == "off":
        STATE = "off"
    else:
        logger.error("Incorrect payload")


if __name__ == "__main__":
    config = Config.from_json_file(os.getenv("DEVICE_CONFIG_PATH", "/etc/mqtt-device/config.json"))

    client = mqtt.Client(userdata=config)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(config.broker_address, 1883, 60)

    client.loop_start()

    while True:
        client.publish(f"{config.topic_base}/state", STATE.encode())
        if config.extra_param == "temp":
            client.publish(f"{config.topic_base}/temp", TEMP)
        if config.extra_param == "rpm":
            client.publish(f"{config.topic_base}/rpm", RPM)
        if config.extra_param == "color_temp":
            client.publish(f"{config.topic_base}/ct", COLOR_TEMP)
        sleep(2)
