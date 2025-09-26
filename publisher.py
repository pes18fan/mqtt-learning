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
        logger.error(f"Bad connection, reason: {CONNACK_CODES[rc]}")


def on_disconnect(client, userdata, rc):
    logger.info(f"Disconnecting, reason: {rc}")


def on_publish(client, userdata, mid):  # create function for callback
    logger.info(f"Data published, MID={mid}")


client = mqtt.Client()  # create new instance
client.on_connect = on_connect  # bind callback functions
client.on_disconnect = on_disconnect
client.on_publish = on_publish


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

ret = client.publish("/topic/qos0", "some data")
while not ret.is_published():
    logger.info("Waiting for publication...")
    time.sleep(1)

ok, mid = ret
if ok != 0:
    logger.error(f"Failed to publish with error code {ok}")
else:
    logger.info(f"Queued publication of MID={mid}")

client.disconnect()
while client.is_connected():
    logger.info("Waiting to disconnect...")
    time.sleep(1)

client.loop_stop()  # Stop loop
