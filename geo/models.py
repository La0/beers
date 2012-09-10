from django.db import models
import geojson
from helpers import nameize

class Localisation(models.Model):
  geojson = models.TextField()
  
  class Meta:
    abstract = True
  
  def get_point(self):
    point = geojson.loads(self.geojson)
    if point['type'] != 'Point':
      return None
    return point['coordinates']

class City(Localisation):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, blank=True)
  zipcode = models.CharField(max_length=10)

  def __unicode__(self):
    return self.name

  def save(self, *args, **kwargs):
    self.urlName = nameize(self.name)
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
