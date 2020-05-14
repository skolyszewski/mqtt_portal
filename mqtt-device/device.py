import json
import os
import logging
from dataclasses import dataclass

import paho.mqtt.client as mqtt


STATE = "off"

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]%(message)s", level=logging.DEBUG)


@dataclass
class Config():
    room_name: str
    device_name: str
    broker_address: str

    @classmethod
    def from_json_file(cls, path):
        with open(path) as f:
            config = json.load(f)

        return cls(
            config["room_name"],
            config["device_name"],
            config["broker_address"],
            )


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to broker with result code {str(rc)}")
    # Subscribe to on/off topic
    client.subscribe(_build_topic(userdata))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logger.info(f"Received message on topic {msg.topic}: {str(msg.payload)}")
    handle_on_off(str(msg.payload))


def handle_on_off(payload):
    global STATE
    if payload == "on":
        STATE = "on"
    elif payload == "off":
        STATE = "off"
    else:
        logger.error("Incorrect payload")


def publish_state(topic, message):
    global STATE


def _build_topic(config):
    return f"devices/{config.room_name}/{config.device_name}"


if __name__ == "__main__":
    config = Config.from_json_file(os.getenv("DEVICE_CONFIG_PATH", "/etc/mqtt-device/config.json"))

    client = mqtt.Client(userdata=config)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(config.broker_address, 1883, 60)

    # # Blocking call that processes network traffic, dispatches callbacks and
    # # handles reconnecting.
    # # Other loop*() functions are available that give a threaded interface and a
    # # manual interface.
    # client.loop_forever()

    client.loop_start()

    while True:
        client.publish(_build_topic(config), STATE)
