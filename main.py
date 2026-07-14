# File naming convention:
# <filename> = neo7m
# <filename2> = lc86g

from machine import UART
import time
import gps_info

# Setup uart for communication and to gather information from gps module
# id=2 for gpio 16/17 of esp32
# baudrate=115200 for lc86g
# baudrate=9600 for neo 7m
uart = UART(2, baudrate=9600, rx=16, tx=17)   
filename = "coordinates.txt"


######## Sampling ############
# Many iterations to get a reliable idea of how accurate each module is compared to a reference value (collected from phone gps)
# Counter used to end loop after one hundred iterations
iterations = 100

# Allow 20 minutes (1200 seconds) to pass incase of cold start
# 30 seconds in case of warm start
time.sleep(30)

# Read in information from gps module
while True:
    if uart.any():
        # Message is encoded as bytes so decoding necessary to convert to string
        rawBytes = uart.read()
        rawMessage = rawBytes.decode("utf-8", "ignore")


        cleanedMessage = gps_info.cleanMessage(rawMessage)
        infoDict = gps_info.parseList(cleanedMessage, filename)
        print(infoDict)

        rawMessage = rawBytes.decode("ascii", "ignore")

        cleanedMessage = gps_info.cleanMessage(rawMessage)
        infoDict = gps_info.parseList(cleanedMessage, filename)
        print(infoDict)
    
    # Loop termination condition to end after 100 iterations
    if iterations == 1:
        break

    iterations -= 1
    # Wait 1s between each iteration 
    time.sleep(1)
