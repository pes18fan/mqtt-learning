import paho.mqtt.client as mqtt  # import client library
import time
from logger import logger

CONNACK_CODES = {
    0: "success",
    1: "unacceptable protocol version",
    2: "identifier rejected",
    3: "server unavailable",
    4: "bad user name or password",
    5: "not authorized",
}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected OK")
    else:
        logger.error(f"Bad connection, reason: {rc}")


def on_disconnect(client, userdata, rc):
    logger.info(f"Disconnecting, reason: {rc}")


client = mqtt.Client()  # create new instance
client.on_connect = on_connect  # bind callback functions
client.on_disconnect = on_disconnect


client.loop_start()  # Start loop

try:
    # connect to broker
    client.connect("broker.hivemq.com")
except Exception as e:
    logger.error(f"Failed to connect: {e}")
    exit(1)

# give it time to connect
while not client.is_connected():
    logger.info("Waiting for connection...")
    time.sleep(1)

time.sleep(3)   # do something here, for now all I have is a sleep

client.disconnect()
while client.is_connected():
    logger.info("Waiting to disconnect...")
    time.sleep(1)

client.loop_stop()  # Stop loop
