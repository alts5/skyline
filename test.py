import paho.mqtt.client as mqtt


client = mqtt.Client()
client.connect("localhost",1883,60)
client.publish("ev3/commands", input());
client.disconnect();

