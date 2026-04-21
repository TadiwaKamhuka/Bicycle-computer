from machine import UART
import time

uart = UART(2, baudrate=115200, tx=17) # Setup uart
time.sleep(1.0) # Allow for first message to be received

while uart.any():						# Check if any message is available to parse
    full_message = uart.read().decode() # Decode the message that is of type bytes


sentences = full_message.split('$') # Split all the sentences into an array 
gga = sentences[1] # Select the first sentence (GPGGA)
gga_parts = gga.split(',') # Break up sentence into its core parts

# Used to convert the time to local time GMT+2
utc = gga_parts[1]
hours = str(int(utc[0:2]) + 2)
minutes = utc[2:4]
seconds = utc[4:6]
ftime = f"{hours}:{minutes}:{seconds}"


latitude = gga_parts[2] + "" + gga_parts[3]
longitude = gga_parts[4] + "" + gga_parts[5]
altitude = gga_parts[9] + "" + gga_parts[10]
satellites = gga_parts[7]
print(latitude + " " + longitude + " " + altitude + " " + satellites + " satellites")
print(ftime)