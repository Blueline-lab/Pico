import paho.mqtt.client as mqtt
import time


class Mqttpublisher:
    def __init__(self):
        self.MQTT_BROKER_ADDR = ""
        self.MQTT_PUBLISH_TOPIC = ""
        self.data = ""
 
        
 

 
    def connect(self):
        self.mqttc = mqtt.Client()
        self.mqttc.connect(self.MQTT_BROKER_ADDR, port=1884)

 
    def publish(self):
        self.mqttc.publish(self.MQTT_PUBLISH_TOPIC, self.data)
        
  