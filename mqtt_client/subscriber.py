import paho.mqtt.client as mqtt
import json
from tinydb import TinyDB, Query
db = TinyDB('../database/db.json')

# MQTT broker details
broker = "158.180.44.197"
port = 1883

# Topics
topic = "iot1/teaching_factory_fast/"

subT_disp_red = "dispenser_red"
subT_disp_green = "dispenser_green"
subT_disp_blue = "dispenser_blue"
subT_recipe = "recipe"
subT_temp = "temperature"
subT_scale = "scale"
subT_drop_vibr = "drop_vibration"
subT_ground_truth = "ground_truth"

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Set username and password for the MQTT broker
mqttc.username_pw_set("bobm", "letmein")

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