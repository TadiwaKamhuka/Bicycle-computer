import matplotlib.pyplot as plt
import math
import numpy as np
import json

def distanceError(lat1, lon1, lat2, lon2):
    
    meters_per_degree = 111320
    
    lat_scale = meters_per_degree
    lon_scale = meters_per_degree * math.cos(math.radians(lat1))

    dx = (lon2 - lon1) * lon_scale
    dy = (lat2 - lat1) * lat_scale

    return math.hypot(dx, dy)

def analyseDevice(device_name,latitudes, longitudes, control_lat, control_lon):
    errors = []

    for lat, lon in zip(latitudes,longitudes):
        errors.append(distanceError(control_lat, control_lon, lat, lon))

    return {
            "Device": device_name,
            "Mean error": float(np.mean(errors)), 
            "Median error": float(np.median(errors)),
            "Maximum error": float(np.max(errors)),
            "RMSE": float(np.sqrt(np.mean(np.array(errors)**2))), 
            "Std dev": float(np.std(errors)),
            "CEP95": float(np.percentile(errors,95))}

def extractCoords(filename):
    latitudes = []
    longitudes = []

    with open(filename) as f:
        for line in f:
            lat, lon = map(float, line.strip().split(","))
            latitudes.append(lat)
            longitudes.append(lon)

    return latitudes, longitudes

def saveAnalysis(results, filename):
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)

def plotDevice(device_name, latitudes, longitudes, control_lat, control_lon, output_file):
    fig = plt.figure(edgecolor="black", layout='constrained')
    axs = fig.subplot_mosaic([['scatter1', 'scatter1'],
                             ['box1', 'box2']])

    # Scatter Plot
    axs['scatter1'].set_title(f"{device_name} Scatter")
    axs['scatter1'].scatter(longitudes, latitudes, label=device_name)
    axs['scatter1'].scatter(control_lon, control_lat, label="control")
    axs['scatter1'].set_xlabel("Longitude")
    axs['scatter1'].set_ylabel("Latitude")
    axs['scatter1'].legend()
    axs['scatter1'].grid(True)

    axs['box1'].set_title("Latitude")
    axs['box1'].boxplot(latitudes)
    axs['box1'].scatter(1, control_lat, label="control latitude")
    axs['box1'].set_xlabel(device_name)
    axs['box1'].set_ylabel("Latitude")
    axs['box1'].grid(True)
    axs['box1'].legend()

    axs['box2'].set_title("Longitude")
    axs['box2'].boxplot(longitudes)
    axs['box2'].scatter(1, control_lon, label="control longitude")
    axs['box2'].set_xlabel(device_name)
    axs['box2'].set_ylabel("Longitude")
    axs['box2'].grid(True)
    axs['box2'].legend()

    plt.savefig(output_file)
    plt.close()

filename = "coordinates.txt"
device_name = "neo7m"  # Change this to "lc86g" for the other device

# Neo 7M control coordinates
control_lat = 47.530909
control_lon = 21.618947
# LC86G control coordinates
control_lat2 = 47.530911
control_lon2 = 21.618952

latitudes, longitudes = extractCoords(filename)
results = analyseDevice(device_name, latitudes, longitudes, control_lat, control_lon)
plotDevice(device_name, latitudes, longitudes, control_lat, control_lon, f"{device_name}_graph.png")

saveAnalysis(results, f"{device_name}_analysis.json")
