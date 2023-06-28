from datetime import datetime
import os
from influxdb_client import WritePrecision, InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import time



class Lora_data_saver:
    
    def __init__(self):
        self.INFLUX_TOKEN = os.environ.get("INFLUXDB_TOKEN")
        self.ORG = "Test" #Organisation define in Influxdb startup configuration
        self.INFLUX_DB_URL = "http://localhost:8086"
        self.BUCKET = "metrics" #Table in InfluxDB
        self.data_postion = {"latitude": 43.856616,"longitude" : 2.3522449, "satelites": 5}
        


    def send_data(self):
        with InfluxDBClient(url=self.INFLUX_DB_URL, token=self.INFLUX_TOKEN, org=self.ORG, debug=False) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
   
            for value in range(5):
                point = (
                Point("GPS_Location")
		        .tag("tag1", "GPS")
                .field("field1", self.data_postion["latitude"])
                .field("field2", self.data_postion["longitude"])
                )
                write_api.write(bucket=self.BUCKET, org=self.ORG, record=point)
                time.sleep(1) 

object = Lora_data_saver()
object.send_data()
