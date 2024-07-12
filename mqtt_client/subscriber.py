import paho.mqtt.client as mqtt
import json
import configparser
from tinydb import TinyDB, Query
db = TinyDB('../database/db.json')

config = configparser.ConfigParser()
config.read('config.ini')

password = config['login']['password']
username = config['login']['username']

# MQTT broker details
broker = config['MQTT']['broker']
port = config['MQTT']['port']

# Topics
topic = config['Topics']['topic']

subT_disp_red = config['Topics']['subT_disp_red']
subT_disp_green = config['Topics']['subT_disp_green']
subT_disp_blue = config['Topics']['subT_disp_blue']
subT_recipe = config['Topics']['subT_recipe']
subT_temp = config['Topics']['subT_temp']
subT_scale = config['Topics']['subT_scale']
subT_drop_vibr = config['Topics']['subT_drop_vibr']
subT_ground_truth = config['Topics']['subT_ground_truth']

#print all of the config readouts -DEBUG-
#print(password)
#print(username)
#print(topic)
#print(subT_disp_red)
#print(subT_disp_green)
#print(subT_disp_blue)
#print(subT_recipe)
#print(subT_temp)
#print(subT_scale)
#print(subT_drop_vibr)
#print(subT_ground_truth)


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Set username and password for the MQTT broker
mqttc.username_pw_set(username, password)

def store_data(payload_dict, topic):
    if not db.table(topic):
        db.table(topic)
    db.table(topic).insert(payload_dict)


# Define the callback function for when a message is received
def on_message(client, userdata, message):
    print("Message received:")
    print("Topic: ", message.topic)
    try:
        # Try to decode the payload and convert to a dictionary
        payload_dict = json.loads(message.payload.decode())
        print("Payload as dictionary: ", payload_dict)
        print(type(payload_dict))

        store_data(payload_dict, message.topic)

    except json.JSONDecodeError:
        # If decoding fails, print an error message
        print("Failed to decode JSON payload.")
    print("\n")

# Assign the callback function to the MQTT client
mqttc.on_message = on_message

# Connect to the MQTT broker
mqttc.connect(broker, port)

# Subscribe to the topic
mqttc.subscribe(topic + subT_disp_red)
mqttc.subscribe(topic + subT_disp_green)
mqttc.subscribe(topic + subT_disp_blue)
mqttc.subscribe(topic + subT_recipe)
mqttc.subscribe(topic + subT_temp)
mqttc.subscribe(topic + subT_scale)
mqttc.subscribe(topic + subT_drop_vibr)
mqttc.subscribe(topic + subT_ground_truth)

# Start the loop to process incoming messages
mqttc.loop_start()

# Keep the script running
try:
    while True:
        pass  # Infinite loop to keep the script running
except KeyboardInterrupt:
    print("Disconnecting from broker...")
    mqttc.loop_stop()
    mqttc.disconnect()
    print("Disconnected.")