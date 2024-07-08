#Код отправителя
import paho.mqtt.client as mqtt
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.motor import MoveTank,OUTPUT_B,OUTPUT_C,SpeedPercent
from ev3dev2.sensor.lego import TouchSensor #UltrasonicSensor
from time import sleep
#Конфигуратор
sound = Sound()
btn = Button()
ts = TouchSensor()
#us = UltrasonicSensor()
motors = MoveTank(OUTPUT_B,OUTPUT_C)
host = '192.168.43.42'

def on_connect(client, userdata, flags, rc):  
    client.subscribe("ev3/commands")
    sound.beep()

def on_message(client, userdata, msg):
    #if us.distance_centimeters < 26:
     #   motors.off()
      #  sound.beep()
       # sleep(10)
        #motors.on(40,-40)    
    if msg.payload.decode() == "BeepOn":
        sound.beep()
    if msg.payload.decode() == "Stop":
        motors.off()
        sleep(3)
        motors.on(-40, 40)
        ts.wait_for_pressed()
        motors.off()
    
    if msg.payload.decode() == "decreaseBegin":
        motors.on(30,-30)
    if msg.payload.decode() == "decreaseFinish":
        motors.on(40, -40)
        
    if msg.payload.decode() == "/start":
        sleep(3)
        motors.on(40, -40)

client = mqtt.Client()
client.connect(host,1883,5)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()

