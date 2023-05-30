from machine import Pin, UART, I2C
import utime, time


class GPS:
    def __init__(self):
        self.gpsModule = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    
        self.buff = bytearray(255)

        self.TIMEOUT = False
        self.FIX_STATUS = False
        self.dict_gps_value = {"latitude": "", "longitude" : "", "satelites": "", "time": ""}
        self.latitude = ""
        self.longitude = ""
        self.satellites = ""
        self.GPStime = ""

    def convertToDegree(self, RawDegrees):

        RawAsFloat = float(RawDegrees)
        firstdigits = int(RawAsFloat/100) 
        nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
        Converted = float(firstdigits + nexttwodigits/60.0)
        Converted = '{0:.6f}'.format(Converted) 
        return str(Converted)
    
    def getGPS(self):
        timeout = time.time() + 8 
        while True:
            self.gpsModule.readline()
            self.buff = str(self.gpsModule.readline())
            parts = self.buff.split(',')
    
            if (parts[0] == "b'$GPGGA" and len(parts) == 15):
                if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                    
                
                    self.latitude = self.convertToDegree(parts[2])
                    if (parts[3] == 'S'):
                        self.latitude = -self.latitude
                    self.longitude = self.convertToDegree(parts[4])
                    if (parts[5] == 'W'):
                        self.longitude = -self.longitude
                    self.satellites = parts[7]
                    self.GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                    self.FIX_STATUS = True
                    break
                
            if (time.time() > timeout):
                self.TIMEOUT = True
                break
            utime.sleep_ms(500)

    def format_gps_value(self):
        self.dict_gps_value = {"latitude": self.latitude, "longitude" : self.longitude, "satelites": self.satellites, "time":self.GPStime}
        return self.dict_gps_value
         
       

run = GPS()            
while True:
    r = run.getGPS()
    

    if(run.FIX_STATUS == True):
        print(run.format_gps_value())
        
       
        FIX_STATUS = False
        
    if(run.TIMEOUT == True):
        print("No GPS data is found.")
        TIMEOUT = False
    
    

