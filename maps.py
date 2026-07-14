import googlemaps
import gps_info

# # API KEY
API_KEY = "AIzaSyAvf5xqLrKePJX68-naFxH2Tu8qXqV1cj0"
client = googlemaps.Client(key=API_KEY)
files = [
    ("coordinates.txt", "0xff0000ff"),
    ("coordinates2.txt", "0x00ff00ff")
]

paths = []
markers = []
center = gps_info.fetchResults(files[0][0])[0]
# path = gps_info.fetchResults(filename)
# path_str = "|".join(path)
# center = path[0]
for filename, color in files:
    coords = gps_info.fetchResults(filename)

    # Add a marker at the first point (optional)
    markers.append(f"color:{color}|{coords[0]}")

    # Create a colored path
    paths.append(
        f"color:{color}|weight:5|" + "|".join(coords)
    )


mapper = client.static_map(size=(600,300), zoom=20, scale=2, center=center, markers=markers, path=paths)


with open("maps.png", "wb") as f:
    for chunk in mapper:
        f.write(chunk)