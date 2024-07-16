# the starbucks html is in div data-e2e="locationList"
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import folium

geolocator = Nominatim(user_agent="outage_finder")
f = open("/Users/jackvu/Desktop/PDS/power_outages/venv/starbucks_html.txt", "r")

def get_coordinates(place_name):
    location = geolocator.geocode(place_name)
    return (location.latitude, location.longitude) if location else None

text = str(f.read())
soup = BeautifulSoup(text, "html.parser")
locations = soup.find_all("article")
warnings = soup.find_all("ul")
names = []
coordinates = []
isOpen = []
for location in locations:
    location_warnings = location.find_all("ul", {'data-e2e': 'store-warnings'})
    location_text = location.find_all("p")
    location_open = True
    for item in location_warnings:
        try:
            warning = item.find("span").text
            if warning == "Closed":
                location_open = False
                break
        except:
            continue
    isOpen.append(location_open)
    names.append(location_text[0].text)
    coordinates.append(get_coordinates(location_text[0].text))

for num in range(len(names)):
    print(names[num], isOpen[num])

mymap = folium.Map(location=coordinates[0], zoom_start=12)

for num in range(len(names)):
    if coordinates[num]:
        if isOpen[num]:
            color = "green"
        else:
            color = "red"
        marker = folium.Marker(
            coordinates[num],
            popup=f"The Starbucks at {names[num]} is functioning" if color == "green" else f"The Starbucks at {names[num]} is down",
            icon=folium.Icon(color=color) # if color == "green" else icon2
        ).add_to(mymap)
# if I'm up for it, I can make custom icons for open, closed, each different establishment
save_path = '/Users/jackvu/Desktop/PDS/power_outages/venv/starbucks_map.html'
mymap.save(save_path)
print(f"Map saved to {save_path}")

