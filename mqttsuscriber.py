import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
import paho.mqtt.client as mqtt
 



class Bridge_MQTT_for_INFLUXDB:
    def __init__(self):

        self.TABLE = os.getenv('INFLUXDB_BUCKET')           #Get credential and DB data from local env
        self.CLIENT= InfluxDBClient(url=os.getenv('INFLUXDB_URL')
        self.CONNECTION_TOKEN = os.getenv('INFLUXDB_TOKEN')
        self.ORGANISATION=os.getenv('INFLUXDB_ORG'))
        self.WRITE_API = self.client.write_api() 

        self.MQTT_BROKER_URL = "10.XXX.XXX.XXX"
        self.MQTT_PUBLISH_TOPIC = "detection"
        self.location = "room1/object12"
 
        self.mqttc = mqtt.Client()
        self.mqttc.connect(self.QTT_BROKER_URL, port=1883)          #Defaut common port for non TLS MQTT is 1883
 
    def on_connect(self, client, userdata, flags, rc):
        """ The callback for when the client connects to the broker."""
        print("Connected with result code "+str(rc))

        client.subscribe(self.MQTT_PUBLISH_TOPIC)
 

    def on_message(self, client, userdata, msg):

        point = Point(self.MQTT_PUBLISH_TOPIC).tag("location"), self.location.field("alert", self.location )        #We not include date time here the INFLUXDB database get it by default
        self.WRITE_API.write(bucket=self.TABLE, record=point)
 




def main():
    runner = True
    flux = Bridge_MQTT_for_INFLUXDB()
    while runner:
        try:
            flux.on_connect
            

        except:
            print(Exception)
            print("not connected")

        flux.on_message()