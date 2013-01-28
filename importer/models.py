from django.db import models

class PlaceCategory(models.Model):
  foursquare_id = models.CharField(max_length=24, null=False)
  name = models.CharField(max_length=255)
  parent = models.ForeignKey('PlaceCategory', null=True)
  used = models.BooleanField(default=False)

  def __unicode__(self):
    return u'%s %s' % (self.foursquare_id, self.name)
