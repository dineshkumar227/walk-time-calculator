from flask import Flask
import json
import requests
import os

app = Flask(__name__)


#TODO Convert to self hosting
def geocode(address):
    maps_prefix = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    key = ".json?access_token=" + str(os.getenv("MAPBOX_KEY"))
    address = address.replace(" ", "+")
    response = requests.get(maps_prefix + address + key)
    geocode_json = json.loads(response.text)
    latitude = geocode_json["features"][0]["center"][1]
    longitude = geocode_json["features"][0]["center"][0]
    return str(longitude) + "," + str(latitude)

def call_osrm(address1, address2):
    coordinate1 = geocode(address1)
    coordinate2 = geocode(address2)
    osrm_prefix = "https://api.mapbox.com/directions/v5/mapbox/walking/"
    key = "?access_token=" + str(os.getenv("MAPBOX_KEY"))
    url = osrm_prefix + coordinate1 + ";" + coordinate2 + key
    osrm = requests.get(url)
    osrm_json = json.loads(osrm.text)
    time = osrm_json["routes"][0]["duration"] / 60
    
    return time

@app.route('/<string:address>')
def get_time(address):
    if len(address.split(';')) == 2:
        address1, address2 = address.split(';')
        return json.dumps(call_osrm(address1, address2))
    else:
        return "Invalid input"

if __name__ == '__main__':
    app.run(debug=True)
