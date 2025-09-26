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


def on_subscribe(client, userdata, mid, granted_qos):
    logger.info(f"Subscribed, MID={mid}")


def on_message(client, userdata, message):
    logger.info(f"Message received:  {str(message.payload.decode(
        "utf-8"))}, topic: {message.topic}, retained: {message.retain}")
    if message.retain == 1:
        logger.info("This is a retained message")


client = mqtt.Client()  # create new instance
client.on_connect = on_connect  # bind callback functions
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message


client.loop_start()  # Start loop

try:
    client.connect("broker.hivemq.com")  # connect to broker
except Exception as e:
    logger.error(f"Failed to connect: {e}")
    exit(1)

# give it time to connect
while not client.is_connected():
    logger.info("Waiting for connection...")
    time.sleep(1)

ret = client.subscribe("house/bulb1")
ok, mid = ret
if ok != mqtt.MQTT_ERR_SUCCESS:
    logger.error(f"Failed to subscribe with code {ok}")
else:
    logger.info(f"Queued subscription of MID={mid}")
time.sleep(2)   # wait for subscription

logger.info("Waiting for a message...")
while True:
    pass

client.loop_stop()
