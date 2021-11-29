from paho.mqtt import client as mqtt
import ssl
import logging

# logging.basicConfig(level=logging.DEBUG)

# Get the IoT Connector ID
try:
    with open("connector_id.txt", "r") as connector_file:
        print("File 'connector_id.txt' found...")
        connector_id = connector_file.read()
except FileNotFoundError as exc:
    print("File 'connector_id.txt' not found...")
    exit()

# Get the Device ID
try:
    with open("device_id.txt", "r") as device_file:
        print("File 'device_id.txt' found...")
        device_id = device_file.read()
except FileNotFoundError as exc:
    print("File 'device_id.txt' not found...")
    exit()

print("\nUsing IoT Connector ID: {}".format(connector_id))
print("\nUsing Device ID: {}".format(device_id))

host = "{}.m2.exosite-staging.com".format(connector_id)
cert = "./Murano_Selfsigned_Root_CA.cer"
# cert = "./DigiCertGlobalRootCA.cer"

def on_connect(client, userdata, flags, rc):
    provision_topic = "$provision/{}".format(device_id)
    client.publish(provision_topic, None, qos=0)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()

    if '$provision/' in msg.topic:
        topic, identity = msg.topic.split('/')

    if topic == "$provision" and payload:
        print("\nIdentity '{}' successfully provisioned!".format(identity))
        print("Cloud-Generated Token: {}".format(payload))
        open('token.txt', "w").write(payload)

    client.disconnect()

def on_disconnect(client, userdata, rc):
    if rc != 0:
        # Unexpected disconnect
        print("\nDisconnected with error: {}".format(rc))
        exit()

client = mqtt.Client(client_id="")
logger = logging.getLogger(__name__)
client.enable_logger(logger)

# Ref: https://github.com/eclipse/paho.mqtt.python/blob/1.1/README.rst#tls_set
client.tls_set(
    ca_certs=cert,
    cert_reqs=ssl.CERT_REQUIRED
)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(host, 8883)
client.loop_forever()