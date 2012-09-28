# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from places.models import Place
from geo.models import City
from django.contrib.auth.models import User
from scrapy.exceptions import DropItem
from scrapper.settings import DJANGO_USER_ID
from places.models import Place
from geo.geocoding import AddressFinder
import geojson
 
class PlacePipeline(object):
  _creator = None

  def __init__(self):
    self._creator = User.objects.get(pk=DJANGO_USER_ID)

  def process_item(self, item, spider):
    # Check we don't already have this bar or this address
    # A bit dummy ... :/
    bars = Place.objects.filter(name__icontains=item['name'])
    if len(bars) > 0:
      raise DropItem('Existing bar by name')
    bars = Place.objects.filter(address=item['address'])
    if len(bars) > 0:
      raise DropItem('Existing bar by address')

    # This is a bar
    item['type'] = 'bar'

    # Lookup real city
    item['city'], _ = City.objects.get_or_create(name=item['city'])

    # Add creator
    item['creator'] = self._creator

    # Search a geocoded position
    af = AddressFinder(item['address'], item['city'])
    res = af.search()
    from pprint import pprint
    if len(res) == 0:
      raise DropItem('No position found')
    pos = res[0]
    p = geojson.Point([pos['lat'], pos['lon']])
    item['geojson'] = geojson.dumps(p)

    # Find subways & city
    place = item.save()
    place.find_subways()
    place.find_city()
    place.save()

    return item