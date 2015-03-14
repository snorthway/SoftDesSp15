"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import json
import sys
from urllib import quote
from urllib2 import urlopen  # urlopen function (better than urllib version)


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urlopen(url)
    response_json = json.loads(f.read())

    return response_json


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    url = GMAPS_BASE_URL + '?address=' + quote(place_name.join('//'))
    response_json = get_json(url)
    loc_dict = response_json['results'][0]['geometry']['location']
    return (loc_dict['lat'], loc_dict['lng'])


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    url = MBTA_BASE_URL+'?api_key='+MBTA_DEMO_API_KEY+"&lat="+str(latitude)+"&lon="+str(longitude)+"&format=json"
    response = get_json(url)
    nearest_stop = None
    for stop in response['stop']:
        if nearest_stop is not None:
            if stop['distance'] < nearest_stop['distance']:
                nearest_stop = stop
        else:
            nearest_stop = stop

    return stop['stop_name']


def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the
    distance from the given place to that stop.
    """
    return get_nearest_station(*get_lat_long(place_name))


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print find_stop_near(' '.join(sys.argv[1:]))
