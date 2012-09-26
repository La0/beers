from django.db import models
import geojson
from helpers import nameize

class Localisation(models.Model):
  geojson = models.TextField()
  
  class Meta:
    abstract = True
  
  def get_point(self):
    if not self.geojson:
      return None
    point = geojson.loads(self.geojson)
    if point['type'] != 'Point':
      return None
    return (float(point['coordinates'][0]), float(point['coordinates'][1]))

  def get_polygon(self):
    if not self.geojson:
      return None
    polygon = geojson.loads(self.geojson)
    if polygon['type'] != 'Polygon':
      return None
    return polygon['coordinates']

class City(Localisation):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, blank=True)
  zipcode = models.CharField(max_length=10)

  def __unicode__(self):
    return self.name

  def save(self, *args, **kwargs):
    self.slug = nameize(self.name)
    super(Localisation, self).save(*args, **kwargs)

class SubwayStation(Localisation):
  name = models.CharField(max_length=255)
  lines = models.ManyToManyField('SubwayLine', through='SubwayStop', related_name='stations')

  def __unicode__(self):
    return self.name

class SubwayLine(models.Model):
  name = models.CharField(max_length=255)
  color = models.CharField(max_length=6, default="FF0000")

  def __unicode__(self):
    return 'Line %s' % self.name
  
  def get_stations(self):
    return self.stations.all().order_by('subwaystop__position')


class SubwayStop(models.Model):
  station = models.ForeignKey(SubwayStation)
  line = models.ForeignKey(SubwayLine)
  position = models.IntegerField(default=0)
