import json
import os
import logging
from dataclasses import dataclass
from time import sleep

import paho.mqtt.client as mqtt


STATE = "off"

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]%(message)s", level=logging.DEBUG)


@dataclass
class Config():
    broker_address: str
    publish_topic: str
    subscribe_topic: str

    @classmethod
    def from_json_file(cls, path):
        with open(path) as f:
            config = json.load(f)

        return cls(
            config["broker_address"],
            config["publish_topic"],
            config["subscribe_topic"],
            )


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to broker with result code {str(rc)}")
    # Subscribe to on/off topic
    client.subscribe(userdata.subscribe_topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    decoded_payload = msg.payload.decode()
    logger.info(f"Received message on topic {msg.topic}: {decoded_payload}")
    handle_on_off(decoded_payload)


def handle_on_off(payload):
    global STATE
    if payload == "on":
        STATE = "on"
    elif payload == "off":
        STATE = "off"
    else:
        logger.error("Incorrect payload")

# import random
# def random_state():
#     global STATE
#     random_bool = random.choice([True, False])
#     STATE = "on" if random_bool else "off"


if __name__ == "__main__":
    config = Config.from_json_file(os.getenv("DEVICE_CONFIG_PATH", "/etc/mqtt-device/config.json"))

    client = mqtt.Client(userdata=config)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(config.broker_address, 1883, 60)

    client.loop_start()

    while True:
        # random_state()
        client.publish(config.publish_topic, STATE.encode())
        sleep(0.5)
