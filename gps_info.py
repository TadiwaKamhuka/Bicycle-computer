# Clean the string and split it into a list
def cleanMessage(rawMessage):
    return rawMessage.split("$")
        
# Parse list for valueable info
def parseList(cleanMessage, filename): 
    result = {}
    for message in cleanMessage:
    # Message id acquired to select only necessary message type
        message_id = message[2:5]
        
        # GGA message contains most positional data
        if message_id == "GGA":
            gga = message.split(',')
            if len(gga) >= 9:
                result["time"] = gga[1]
                result["latitude"] = gga[2]
                result["latitude_dir"] = gga[3]
                result["longitude"] = gga[4]
                result["longitude_dir"] = gga[5]
                # result["fix"] = gga[6] # Delete after test
                result["satellites"] = gga[7]
                result["altitude"] = gga[9]            

    lat = result.get("latitude")
    lon = result.get("longitude")

    # Store the coordinates into a file so they can be read later
    storeResults(filename, [lat, lon])
    
    return result

# Used to write the coordinates into the file so they can be read later
def storeResults(filename, resultList): 
    # Latitude
    ns = resultList[0]
    # Longitude
    ew = resultList[1] 
    with open(filename, "a") as f:
        f.write(f"{nmeaToDecimal(ns)}, {nmeaToDecimal(ew)}\n")
    
# Convert NMEA coordinates to decimal degrees
def nmeaToDecimal(coord):
    # Check if the coordinate is invalid
    if not coord:
        return None
    # Remove the direction letters from the coordinate
    coord = coord.replace("N", "").replace("S", "").replace("E", "").replace("W", "")
    
    coord = float(coord)
    degrees = int(coord//100)
    minutes = coord - (degrees*100)

    return degrees + minutes/60

# filename parameter must receive an already opened file
def fetchResults(filename):
    path = []

    with open(filename, "r") as f:
        for line in f:
            coord = line.strip()
            lat, lon = coord.split(",")
            path.append(f"{lat.strip()},{lon.strip()}")

    return path