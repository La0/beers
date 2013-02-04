from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from geo.models import City
from bars.settings import FOURSQUARE_CLIENT, FOURSQUARE_SECRET, INSTAGRAM_CLIENT, INSTAGRAM_SECRET, BOT_USER_ID
from foursquare import Foursquare
from instagram.client import InstagramAPI
from importer.models import PlaceCategory
from places.models import Place
import geojson
from geo.geocoding import CityFinder

class Command(BaseCommand):

  _user = None
  _foursquare = None
  _instagram = None
  _categories = None

  def handle(self, *args, **options):
    if len(args) != 1:
      raise CommandError('Specify a city name')
  
    self.init()

    # Search cities
    search = args[0]
    cities = City.objects.filter(name__contains=search).order_by('name')
    if not len(cities):
      raise CommandError('No cities found for %s' % search)
    for c in cities:
      self.import_city(c)

  def init(self):
    self._foursquare = Foursquare(client_id=FOURSQUARE_CLIENT, client_secret=FOURSQUARE_SECRET)
    self._instagram = InstagramAPI(client_id=INSTAGRAM_CLIENT, client_secret=INSTAGRAM_SECRET)
    self._categories = PlaceCategory.objects.filter(used=True)
    self._user = User.objects.get(pk=BOT_USER_ID)

  def import_city(self, city):
    print 'Importing city %s' % city
    center, radius = city.get_center()

    params = {
      'intent' : 'browse',
      'll' : '%f,%f' % center,
      'radius' : radius,
      'categoryId' : ','.join([c.foursquare_id for c in self._categories]),
    }
    res = self._foursquare.venues.search(params=params)

    for venue in res['venues']:
      try:
        self.import_place(venue, city)
      except Exception, e:
        print 'Import failed for %s : %s' % (venue.get('id', '-'), str(e))

  def import_place(self, venue, search_city):

    categories = self._categories.filter(foursquare_id__in=[c['id'] for c in venue['categories']])
    pos = (float(venue['location']['lat']), float(venue['location']['lng']))
    cf = CityFinder(pos)
    city = cf.search()
    if city is None:
      raise Exception('No city found')
    if city != search_city:
      print 'City mismatch search:"%s" vs. found:"%s"' % (search_city, city)

    location = geojson.Point(pos)

    defaults = {
      'name' : venue['name'],
      'city' : city,
      'creator' : self._user,
      'address' : venue['location'].get('address', ''),
      'geojson' : geojson.dumps(location),
    }
    place, created = Place.objects.get_or_create(foursquare_id=venue['id'], defaults=defaults)
    if not created:
      for k,v in defaults.items():
        setattr(place, k, v)
    place.find_subways()
    place.categories = categories
    place.save()
    print '%s place %d %s' % (created and 'Created' or 'Updated', place.id, place.name)

    from pprint import pprint
    pprint(venue)
