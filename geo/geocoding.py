from urllib import urlencode
from urllib2 import urlopen
import simplejson as json

class AddressFinder:
  _url = "http://nominatim.openstreetmap.org/search"
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
    url = '%s?%s' % (self._url, urlencode(args))
    
    try:
      res = urlopen(url)
      self._data = json.loads(res.readline())
    except Exception, e:
      print 'failed: %s' % (str(e))
    return self._data