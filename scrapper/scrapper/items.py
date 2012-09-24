# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

from scrapy.contrib_exp.djangoitem import DjangoItem
from places.models import Place

class PlaceItem(DjangoItem):
  django_model = Place
