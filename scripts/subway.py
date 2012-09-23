# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime

# Setup django
sys.path.append(os.path.realpath('.'))
from django.core.management import setup_environ
import bars.settings
setup_environ(bars.settings)

# Models
from geo.models import *
import simplejson as json
import geojson
import os

def load_stations(stations):
  for h, station in stations.items():
    # Build or update station
    station['coords'].reverse() # First lat, then lng
    p = geojson.Point(station['coords'])     
    st, created = SubwayStation.objects.get_or_create(geojson=geojson.dumps(p))
    st.name = station['name']
    st.save()
    
    # Build links
    for name, position in station['lines'].items():
      line, _ = SubwayLine.objects.get_or_create(name=name)
      stop, stop_created = SubwayStop.objects.get_or_create(station=st, line=line)
      if stop_created:
        stop.position = position
        stop.save()
    
    print st
  
def main(file):
  # Get stations
  if not os.path.exists(file):
    raise Exception('Source file not found %s' % file)
  f = open(file)
  data = json.loads(f.read())
  f.close()
  if data is None:
    raise Exception('No data in %s' % file)
  load_stations(data)
  
  
if __name__ == '__main__':
  main('scripts/stations.json')