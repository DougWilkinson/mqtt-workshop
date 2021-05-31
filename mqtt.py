import time
import json
from umqtt.simple import MQTTClient
import network
import machine
import dht

# Create a unique client name based on last octect of IP address 
# bdw123
mqttname = "bdw" + str(network.WLAN().ifconfig()[0][-3:]) 

servo = 90
mqttflag = False

def mqtt_cb(topic, message):
    global servo
    global mqttflag
    print(topic,message)
    if topic == b'servo':
        servo = int(message)
        mqttflag = True

def setup():
    
    # This will be different if you setup your own cloudmqtt account
    server = "m16.cloudmqtt.com"
    port = 16135
    client = MQTTClient(mqttname, server, port, user="xxxxx", password="xxxxx")
    
    client.set_callback(mqtt_cb)
    client.connect(clean_session=True)
    client.subscribe(b"+/temperature")
    client.subscribe(b"+/humidity")
    client.subscribe("servo")
    return(client)

def sensor():
    
    client = setup()
    mydht = dht.DHT22(machine.Pin(4))

    lastcheck = time.time()
    while True:
        client.check_msg()
        if time.time() - lastcheck > 10:
            mydht.measure()
            client.publish(mqttname + "/temperature", str(mydht.temperature()))
            client.publish(mqttname + "/humidity", str(mydht.humidity()))
            lastcheck = time.time()

def servo():
    global mqttflag
    client = setup()
    myservo = machine.PWM(machine.Pin(5), 50, 0)
    while True:
        client.check_msg()
        if mqttflag:
            mqttflag = False
            myservo.duty(servo)
            time.sleep_ms(500)
        myservo.duty(0)

