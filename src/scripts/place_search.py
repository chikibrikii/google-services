"""
Created on Mon Mar 27 14:22:50 2017

@author: chsoon

requests to Google Places Web Service API - note that it is non RESTful (no verb definitions)
"""
# !/usr/bin/env python
try:
    import requests
    import simplejson as json
except ImportError:
    import json

key = ''
search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json" 
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

# @app.route{"/sendRequest/<string:query>"}
def results(query):
    search_payload = {"key":key, "query":query}
    
    try:
        search_req = requests.get(search_url, params=search_payload)  # requests module will handle building URL string.
    except requests.exceptions.HTTPError as error:
        print error
    
    search_json = search_req.json()
    place_id = search_json["results"][0]["place_id"]

    # send a details URL using the place_id
    details_payload = {"key":key, "placeid":place_id}
    
    try:
        details_resp = requests.get(details_url, params=details_payload)
    except requests.exceptions.HTTPError as error:
        print error
    
    details_json = details_resp.json()

    url = details_json["result"]["url"]  
    lat_long = details_json["result"]["geometry"]["location"]
    
    return json.dumps({'url' : url, 'lat_long' : lat_long})