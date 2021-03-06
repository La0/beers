from django.db import models
from places.models import Place
from django.contrib.auth.models import User
from helpers import nameize

class ProductCategory(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, blank=True)

  def __unicode__(self):
    return self.name

  def save(self, *args, **kwargs):
    self.slug = nameize(self.name)
    super(ProductCategory, self).save(*args, **kwargs)

class Product(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, blank=True)
  category = models.ForeignKey(ProductCategory, related_name="products")
  brand = models.CharField(max_length=255, null=True, blank=True)

  # Creator
  creator = models.ForeignKey(User)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  # Link to places
  places = models.ManyToManyField(Place, through='ProductPrice')

  # Extra data
  wikipedia = models.URLField(null=True)

  def __unicode__(self):
    return self.name

  def save(self, *args, **kwargs):
    self.slug = nameize(self.name)
    super(Product, self).save(*args, **kwargs)


class ProductPrice(models.Model):
  '''
  Link a Product and a Place
  specifying the price, date, creator...
  '''
  place = models.ForeignKey(Place, related_name='prices')
  product = models.ForeignKey(Product)
  current = models.BooleanField(default=True)

  price = models.FloatField()

  # Creator
  creator = models.ForeignKey(User)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
  