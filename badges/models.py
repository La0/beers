from helpers import nameize
from django.db import models
from django.contrib.auth.models import User
from places.models import Place

class Badge(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, blank=True)

  creator = models.ForeignKey(User)
  created = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.name
  
  def save(self, *args, **kwargs):
    self.slug = nameize(self.name)
    super(Badge, self).save(*args, **kwargs)

  @models.permalink
  def get_absolute_url(self):
    return ('badge-view', [self.slug])


class PlaceBadge(models.Model):
  '''
  Link a Place and a Badge
  '''
  place = models.ForeignKey(Place)
  badge = models.ForeignKey(Badge, related_name='places')
  
  user = models.ForeignKey(User)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = (('place', 'badge'),)