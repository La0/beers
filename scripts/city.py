# -*- coding: utf-8 -*-
import sys
import os

# Setup django
sys.path.append(os.path.realpath('.'))
from django.core.management import setup_environ
import bars.settings
setup_environ(bars.settings)

from xml.dom.minidom import parse

# Models
from geo.models import City
import simplejson as json
import geojson

def get_file():
  if len(sys.argv) != 2:
    raise Exception('Specify a file')
  path = sys.argv[1]
  if not os.path.exists(path):
    raise Exception('File not found %s' % path)
  return path

def load_kml(path):
  xml = parse(path)
  if xml is None:
    raise Exception('No xml in %s' % path)
  marks = xml.getElementsByTagName('Placemark')
  for mark in marks:
    
    try:
      # Extract city name & coords
      city_name = mark.getElementsByTagName('name')[0].firstChild.nodeValue
      city_coords = mark.getElementsByTagName('coordinates')[0].firstChild.nodeValue
      city_coords = [c.strip().split(',') for c in city_coords.split('\n') if c.strip() != '']

      if len(city_coords) <= 1:
        raise Exception('Not enough coordinates')

      # Build city, with geojson
      city,_ = City.objects.get_or_create(name=city_name)
      polygon = geojson.Polygon()
      for lng,lat,_ in city_coords:
        polygon.coordinates.append((float(lat), float(lng)))
      city.geojson = geojson.dumps(polygon)
      city.save()
      
      print 'Saved city #%d %s' % (city.id, city.name)
      
    except Exception, e:
      print 'Bad Placemark: %s' % (str(e),)

if __name__ == '__main__':
  try:
    path = get_file()
    load_kml(path)
  except Exception, e:
    print 'Error: %s' % (str(e),)