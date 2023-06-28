from sx1262 import SX1262
import time
import nmea
trame = b""
sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)

# LoRa
sx.begin(freq=868, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

# FSK
##sx.beginFSK(freq=923, br=48.0, freqDev=50.0, rxBw=156.2, power=-5, currentLimit=60.0,
##            preambleLength=16, dataShaping=0.5, syncWord=[0x2D, 0x01], syncBitsLength=16,
##            addrFilter=SX126X_GFSK_ADDRESS_FILT_OFF, addr=0x00, crcLength=2, crcInitial=0x1D0F, crcPolynomial=0x1021,
##            crcInverted=True, whiteningOn=True, whiteningInitial=0x0100,
##            fixedPacketLength=False, packetLength=0xFF, preambleDetectorLength=SX126X_GFSK_PREAMBLE_DETECT_16,
##            tcxoVoltage=1.6, useRegulatorLDO=False,
##            blocking=True)
obj_get_gps_data = nmea.GPS()
while True:
    run = obj_get_gps_data.getGPS()
    if obj_get_gps_data.FIX_STATUS == True:
        trame+=obj_get_gps_data.format_gps_value()
        sx.send(trame)
        print(obj_get_gps_data.FIX_STATUS)
        obj_get_gps_data.FIX_STATUS = False

    else:
        print("GNSS Module not receiving data")
        sx.send(b'GNSS Module not receiving data')

    time.sleep(10)
