from django.core.management.base import BaseCommand, CommandError
from geo.models import City
from bars.settings import FOURSQUARE_CLIENT, FOURSQUARE_SECRET, INSTAGRAM_CLIENT, INSTAGRAM_SECRET
from foursquare import Foursquare
from instagram.client import InstagramAPI
from importer.models import PlaceCategory

class Command(BaseCommand):

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
        print '-'*40
        print '%(id)s %(name)s' % venue
        from pprint import pprint
        pprint(venue)
      except:
        pass
