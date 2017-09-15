# !/usr/bin/env python
import requests
import urllib, urllib2
import pandas as pd
try:
    import simplejson as json    
except ImportError:
    import json

key = ''
search_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
elevation_base_url = 'https://maps.googleapis.com/maps/api/elevation/json'
# CHART_BASE_URL = 'https://chart.apis.google.com/chart'


def getPoints(startpoint, endpoint):
    try:
        startsearch_payload = {'key':key, 'query':startpoint}
        startsearch_req = requests.get(search_url, params=startsearch_payload)
    except requests.exceptions.HTTPError:
        print 'error'
    startsearch_json = startsearch_req.json()
    startpoint_coords = startsearch_json['results'][0]['geometry']['location']
    
    try:
        endsearch_payload = {'key':key, 'query':endpoint}
        endsearch_req = requests.get(search_url, params=endsearch_payload)
    except requests.exceptions.HTTPError:
        print 'error'
    endsearch_json = endsearch_req.json()
    endpoint_coords = endsearch_json['results'][0]['geometry']['location']
    
    all_coords = json.dumps({'startpoint':startpoint_coords, 'endpoint':endpoint_coords})
    
    path = "%s,%s|%s,%s"%(startpoint_coords['lat'], startpoint_coords['lng'],
                            endpoint_coords['lat'], endpoint_coords['lng'])
    
    return path


def getElevation(path, samples='500', **elvtn_args):
    elvtn_args.update({
            'path' : path,
            'samples' : samples
        })
    url = elevation_base_url + '?' + urllib.urlencode(elvtn_args)
    response = json.load(urllib.urlopen(url))
    
    elevationArray = []
    
    for resultset in response["results"]:
        elevationArray.append(resultset["elevation"])

    return elevationArray


def getCoordsElvn(origin, destination):
    latlng = getPoints(origin, destination)
    elevation = getElevation(latlng)
    
    return latlng, elevation