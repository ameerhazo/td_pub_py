# from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import time
import random
import os
import time

broker = '192.168.176.87'
port = 1883
basetopic = "things/"
client_id = "mqtt-client"
username = "mqtt"
password = "mqtt"

def read_file_list():
    entries = os.listdir('.')
    filtered = list(filter(lambda e: e.startswith("Multisensor"),entries))
    return filtered

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

def connect_mqtt():
    # Set Connecting Client ID
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client,id,data):
    topic = basetopic + id
    print(f'Publishing {len(data)} bytes to topic: {topic}')
    result = client.publish(topic, payload=data, qos=0, retain=True)
    #result: [0, 1]
    status = result[0]
    if status == 0:
       print(f"Send data for `{id}` to topic `{topic}`")
    else:
       print(f"Failed to send message to topic {topic}")

client = None
client = connect_mqtt()
client.loop_start()

tds = read_file_list()
print(f'Found TDs: {tds}')
for t in tds:
    with open(t, 'r') as file:
        data = file.read()
        # print(data)
        id = t.split('_')[1][:-5]
        publish(client,id,data)
        time.sleep(1)
