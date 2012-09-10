from django.db import models
from geo.models import Localisation, City
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