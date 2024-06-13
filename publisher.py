import paho.mqtt.client as mqtt
broker = "158.180.44.197"
port = 1883

topic_groupname = "aut/RuabnZuzzler/$groupname"
topic_names = "aut/RuabnZuzzler/names"

names = "Peer/Thöni/Unterhuber"
groupname = "RuabnZuzzler"



# create client object
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set("bobm", "letmein")       

                
# establish connection
mqttc.connect(broker,port)          

mqttc.publish(topic_groupname, groupname)
mqttc.publish(topic_names, names)



while True:
    mqttc.loop(0.5)
    