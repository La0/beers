from django.db import models
from geo.models import Localisation, City, SubwayStation
from django.contrib.auth.models import User
from helpers import nameize
from geo.geocoding import CityFinder

PLACE_TYPE = (
  ('bar', 'Bar'),
  ('restaurant', 'Restaurant'),
)

class Place(Localisation):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, blank=True)
  type = models.CharField(max_length=10, choices=PLACE_TYPE, default='bar')
  address = models.CharField(max_length=255)
  city = models.ForeignKey(City, related_name='places')
  subways = models.ManyToManyField(SubwayStation, blank=True)
  badges = models.ManyToManyField('badges.Badge', through='badges.PlaceBadge', blank=True)
  
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
    super(Localisation, self).save(*args, **kwargs)

  def find_city(self):
    '''
    Find the city of a place, using it's coordinates
    and the CityFinder algorithm (fast)
    '''
    cf = CityFinder(self)
    city = cf.search()
    if city is not None:
      self.city = city

  def find_subways(self, max_distance = 15):
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

    # Clean stations
    self.subways.all().delete()

    stations = SubwayStation.objects.all() # BAD !
    for station in stations:
      station_lat, station_lng = station.get_point()
      lat_diff = abs(lat - station_lat) * POI_ORTHO_BASE
      lng_diff = abs(lng - station_lng) * POI_ORTHO_BASE
      diff = math.ceil(math.sqrt(lat_diff**2 + lng_diff**2))
      if diff > max_distance:
        continue
      self.subways.add(station)
  
  def get_hours_per_days(self):
    '''
    Give the hours per days, linking hh and normal hours
    '''
    days = [{'id' : d, 'name' : n} for d,n in WEEK_DAYS]
    hours = self.hours.all()
    for h in hours:
      hour_type = h.happy_hour and 'happy_hour' or 'normal'
      days[int(h.day)][hour_type] = h    
    return days
    

WEEK_DAYS = (
  (0, 'Monday'),
  (1, 'Tuesday'),
  (2, 'Wednesday'),
  (3, 'Thursday'),
  (4, 'Friday'),
  (5, 'Saturday'),
  (6, 'Sunday'),
)

class PlaceHour(models.Model):
  place = models.ForeignKey(Place, related_name='hours')
  day = models.CharField(max_length=1, choices=WEEK_DAYS)
  start = models.TimeField()
  end = models.TimeField()
  happy_hour = models.BooleanField(default=False)

  class Meta:
    unique_together = ('place', 'day', 'happy_hour')

LINK_TYPE = (
  ('official', 'Official'),
  ('article', 'Article'),
  ('social', 'Social (Fb,...)'),
)

class PlaceLink(models.Model):
  place = models.ForeignKey(Place, related_name='links')
  url = models.URLField()
  title = models.CharField(max_length=255, null=True, blank=True)
  type = models.CharField(max_length=10, choices=LINK_TYPE, default='article')
  creator = models.ForeignKey(User)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('place', 'url')

  def search_title(self):
    '''
    Search title from web page
    '''
    if self.url is None:
      raise Exception('No url specified')
    try:
      import urllib
      import BeautifulSoup
      soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(self.url))
      self.title = soup.title.string.strip()
    except Exception, e:
      print str(e)
      return False
    return True

  def get_domain(self):
    '''
    Quickly extract the domain name of the link
    '''
    from urlparse import urlparse
    p = urlparse(self.url)
    return p.netloc.startswith('www.') and p.netloc[4:] or p.netloc