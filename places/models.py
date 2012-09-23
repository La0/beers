from django.db import models
from geo.models import Localisation, City, SubwayStation
from django.contrib.auth.models import User
from helpers import nameize

PLACE_TYPE = (
  ('bar', 'Bar'),
  ('restaurant', 'Restaurant'),
)

class Place(Localisation):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, blank=True)
  type = models.CharField(max_length=10, choices=PLACE_TYPE, default='bar')
  address = models.CharField(max_length=255)
  city = models.ForeignKey(City)
  subways = models.ManyToManyField(SubwayStation)
  
  # Creator
  creator = models.ForeignKey(User)
  created = models.DateTimeField(auto_now_add=True)
  modified =models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return self.name

  @models.permalink
  def get_absolute_url(self):
    return ('place-view', [self.city.slug, self.slug])

  def save(self, *args, **kwargs):
    self.slug = nameize(self.name)

    # Update subways
    if self.geojson is not None:
      self.find_subways()

    super(Localisation, self).save(*args, **kwargs)

  def find_subways(self, max_distance = 10):
    '''
    Bad implementation, we should be able to limit the perimeter
    of research...
    '''
    import math
    POI_ORTHO_BASE = 1852

    pos = self.get_point()
    if pos is None:
      return False
    lat, lng = pos

    stations = SubwayStation.objects.all() # BAD !
    for station in stations:
      station_lat, station_lng = station.get_point()
      lat_diff = abs(lat - station_lat) * POI_ORTHO_BASE
      lng_diff = abs(lng - station_lng) * POI_ORTHO_BASE
      diff = math.ceil(math.sqrt(lat_diff**2 + lng_diff**2))
      if diff > max_distance:
        continue
      self.subways.add(station)
    self.save()