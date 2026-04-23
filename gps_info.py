from machine import UART, Pin
import time

# Setup uart for communication and to gather information from gps module
# id=2 for gpio 16/17
uart = UART(2, baudrate=115200, rx=16, tx=17)
gps_data = {"module": []}

# Go through the message recieved from gps and put it in a usable format
def parseSerialMessage(rawMessage):
    # Use the pdop value from first GSA sentence
    pdopCount = 0
    
    # Clean the string and split it into a list
    if rawMessage[0:2] == "b'":
        rawMessage = rawMessage.lstrip("b'").rstrip("'")
    messages = rawMessage.split("$")
        
    result = {}
    
    for message in messages:
        # Message id acquired to select only necessary messages
        message_id = message[2:5]
        
        # GGA message contains most positional data
        if message_id == "GGA":
            gga = message.split(',')
            result["time"] = gga[1]
            result["latitude"] = gga[2] + gga[3]
            result["longitude"] = gga[4] + gga[5]
            result["satellites"] = int(gga[7])
            result["altitude"] = gga[9] + gga[10]
        
        # GSA contains satellite data and data for accuracy checking
        if message_id == "GSA":
            gsa = [g for g in message.split(',') if g != '']
            
            # Only record first GSA sentences pdop value
            if pdopCount == 0:
                result["pdop"] = gsa[-4]
                pdopCount += 1
            
    return result

######## Validation/Testing ############
# Counter used to end loop after three iterations
iterations = 1

# Allow 30 seconds to pass incase of cold start
time.sleep(30)

# Read in information from gps module
while True:
    if uart.any():
        # Message is encoded as bytes so decoding necessary to convert to string
        rawMessage = uart.read().decode()
        measurement = parseSerialMessage(rawMessage)
        print(measurement)
        gps_data["LC86G"].append(measurement)

    if iterations == 4:
        break
    else:
        iterations += 1
        # 300s / 5m used to measure precision at different times
        time.sleep(300)
        