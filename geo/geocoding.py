from urllib import urlencode
from urllib2 import urlopen
import simplejson as json
from geo.models import City
import sys

class AddressFinder:
  _url = u"http://nominatim.openstreetmap.org/search"
  _address = ''
  _data = []
  
  def __init__(self, address, city):
    if address == '':
      raise Exception("Empty address")
    self._address = u'%s, %s' % (address, city.name)
  
  def search(self):
    '''
    Search on OpenStreetMap geocoding service
    '''
    args = {
      'format' : 'json',
      'q' : self._address,
      'countrycodes' : 'fr', # Harccoded !
    }

    try:
      url = '%s?%s' % (self._url, urlencode(args))
      res = urlopen(url)
      self._data = json.loads(res.readline())
    except Exception, e:
      print 'failed: %s' % (str(e))
    return self._data

class CityFinder:
  _lat = 0.0
  _lng = 0.0

  def __init__(self, place):
    point = place.get_point()
    if point is None:
      raise Exception('No coordinates')
    self._lat, self._lng = point

  def search(self):
    '''
    Search the city of a place, using coordinates
    Raycasting: http://en.wikipedia.org/wiki/Point_in_polygon | http://rosettacode.org/wiki/Ray-casting_algorithm
    '''
    cities = City.objects.exclude(geojson='')
    for city in cities:
      polygon = city.get_polygon()
      if polygon is None:
        continue

      # Search first intersection for each side
      # on odd intersections, we are in !
      s = sum(self._ray_intersect(polygon[i], polygon[i+1]) for i in range(0, len(polygon) - 1))
      if s % 2 == 1:
        return city

    return None

  def _ray_intersect(self, a, b):
    _huge = sys.float_info.max
    _tiny = sys.float_info.min

    # Point A must be below Point b
    if a[0] > b[0]:
      a,b = b,a

    # Useful here ?
    if self._lat == a[0] or self._lat == b[0]:
      self._lat += 0.0001

    intersect = False

    if (self._lat > b[0] or self._lat < a[0]) or (self._lng > max(a[1], b[1])):
      return False

    if self._lng < min(a[1], b[1]):
      intersect = True
    else:
      if abs(a[1] - b[1]) > _tiny:
        m_red = (b[0] - a[0]) / float(b[1] - a[1])
      else:
        m_red = _huge
      if abs(a[1] - self._lng) > _tiny:
        m_blue = (self._lat - a[0]) / float(self._lng - a[1])
      else:
        m_blue = _huge
      intersect = m_blue >= m_red

    return intersect