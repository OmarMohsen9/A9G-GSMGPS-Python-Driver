'''
This is a Python driver for A9G (GSM/GPRS+GPS Development Board)
Tested on Windows/raspberry Pi 3B & 4B  with USB to TTL converters (Tested on PL2303 & CH340 modules)
Connection : Tx of Gps/Gsm to Rx of Usb to ttl ///  Tx of Usb to ttl to Rx of Gps/Gsm
This driver should be used the same way AI-Thinker serial tool(SW app for running AT Commands) is used
'''
import serial
import time

print("initializing...")
#defining serial instance
#win
ser = serial.Serial('COM6', baudrate=9600, timeout=1)
#linux/darwin
# ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

#Set Phone Number
phone_number = "+201234567890"

def gsm_handshake():
    while True:
        ser.write(b"AT\r")
        print(ser.readline())
        test=ser.readline()
        print(test)
        listtest = b'OK\r\n'
        if test == listtest:
            break
    time.sleep(5)


def gsm_callnumber():
    gsm_handshake()
    ser.write('ATD"{}";\r'.format(phone_number).encode('utf-8'))
    print(ser.readlines())
    time.sleep(20)
    ser.write(b"ATH\r")
    print(ser.readlines())


def gsm_sendsms():
    gsm_handshake()
    ser.write(b"AT+CMGF=1\r")
    print(ser.readlines())
    ser.write('AT+CMGS="{}" \r '.format(phone_number).encode('utf-8'))
    ser.write(b'Hello there\x1A')
    print(ser.readlines())
    time.sleep(1)
    print(ser.readlines())


def gsm_checksim():
    gsm_handshake()
    ser.write(b'AT+CSQ\r')
    print(ser.readlines())
    ser.write(b'AT+CCID\r')
    print(ser.readlines())
    ser.write(b'AT+CREG?\r')
    print(ser.readlines())

def gps_sendlocation():
    gsm_handshake()
    ser.write(b'AT+GPS=1\r')
    #print(ser.readlines())
    ser.write(b'AT+GPSRD=2\r')
    time.sleep(2.5)
    #ser.write(b'AT+LOCATION=2\r')
    x=ser.readlines()
    if b'AT+GPSRD=2\r\r\n' in x:
        y = x[9:]
        i = 0
        j = len(y)
        while i <= j:
            y[i] = y[i].decode("utf-8")
            if "$GNRMC" in y[i]:
                part = y[i]
                f = part[20:44]
                latitude = float(f[0:2]) + float(f[2:9]) / 60
                latitude = round(latitude, 4)
                latitude_direction = f[10:11]
                longitude = float(f[12:15]) + float(f[15:22]) / 60
                longitude = round(longitude, 4)
                longitude_direction = f[23:24]
                location_details = [str(latitude) + latitude_direction, str(longitude) + longitude_direction]
                location_details = ",".join(location_details)
                print("https://maps.google.com/?q=" + location_details)
                break
            else:
                i += 1
    ser.write(b'AT+GPS=0\r')
    print(ser.readlines())


def gps_receivemode():
    gsm_handshake()
    ser.write(b'AT+CMGF=1\r')
    print(ser.readlines())
    ser.write(b'AT+CNMI=1,2,0,0,0\r')
    print(ser.readlines())


