from paho.mqtt import client as mqtt
import ssl
import logging
import time
import json

# logging.basicConfig(level=logging.DEBUG)

try:
    with open("connector_id.txt", "r") as connector_file:
        print("Local 'connector_id.txt' file found...")
        connector_id = connector_file.read()
except FileNotFoundError as exc:
    print("No local 'connector_id.txt' file found...")
    connector_id = input("Connector ID? ")
    with open("connector_id.txt", "w") as connector_file:
        connector_file.write(connector_id)

print("Using IoT Connector ID: {}".format(connector_id))
host = "{}.m2.exosite-staging.com".format(connector_id)
cert = "./Murano_Selfsigned_Root_CA.cer"

def on_connect(client, userdata, flags, rc):
    topic = "$resource/config_io"
    value = '{"channels": {"brewing_status": {"display_name": "Brewing Status","description": "","properties": {"data_type": "BOOLEAN","controle": true}}}}'

    print("Publishing value '{}' to topic '{}'".format(value, topic))
    client.publish(topic, value, qos=0)

    print("Done! Disconnecting...")
    client.disconnect()

def on_message(client, userdata, msg):
    print("Cloud-originated message '{}' found for topic '{}'".format(msg.payload.decode(), msg.topic))

def on_disconnect(client, userdata, rc):
    print(rc)
    if rc != 0:
        # Unexpected disconnect
        print("Disconnected with error: {}".format(rc))
        exit()

client = mqtt.Client(client_id="", clean_session=True)
logger = logging.getLogger(__name__)
client.enable_logger(logger)

# Ref: https://github.com/eclipse/paho.mqtt.python/blob/1.1/README.rst#tls_set
client.tls_set(
    ca_certs=cert,
    cert_reqs=ssl.CERT_REQUIRED
)
client.will_set(topic="$resource/config_io", payload="this is from the will", qos=0)

token = open("./token.txt", "r").read()
print("Using Token: {}\n".format(token))
client.username_pw_set("", token)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(host, 8883)
client.loop_forever()