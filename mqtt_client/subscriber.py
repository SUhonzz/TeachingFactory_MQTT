import paho.mqtt.client as mqtt

# MQTT broker details
broker = "158.180.44.197"
port = 1883

# Topics
topic = "iot1/teaching_factory_fast/"

subT_disp_red = "dispenser_red"
subT_disp_green = "dispenser_green"
subT_disp_blue = "dispenser_blue"


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Set username and password for the MQTT broker
mqttc.username_pw_set("bobm", "letmein")

# Define the callback function for when a message is received
def on_message(client, userdata, message):
    print("Message received:")
    print("Topic: ", message.topic)
    print("Payload: ", message.payload.decode())
    print("\n")
    print(message.payload)

# Assign the callback function to the MQTT client
mqttc.on_message = on_message


#print("topic_groupname: ", topic_groupname)
# Connect to the MQTT broker
mqttc.connect(broker, port)

# Subscribe to the topic
mqttc.subscribe(topic + subT_disp_red)
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
