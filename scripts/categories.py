# -*- coding: utf-8 -*-
import sys
import os

# Setup django
sys.path.append(os.path.realpath('.'))
from django.core.management import setup_environ
import bars.settings
setup_environ(bars.settings)

from bars.settings import FOURSQUARE_CLIENT, FOURSQUARE_SECRET

# Models
from importer.models import PlaceCategory 
import simplejson as json

# Api
from foursquare import Foursquare
foursquare = Foursquare(client_id=FOURSQUARE_CLIENT, client_secret=FOURSQUARE_SECRET)

# Cache categories
def cache_categories(name):
  if os.path.exists(name):
    print 'Using cached categories from %s' % name
    return json.load(open(name, 'r'))

  print 'Loading fresh categories...'
  res = foursquare.venues.categories()
  f = open(name, 'w') 
  f.write(json.dumps(res))
  return res

def save_category(cat, parent=None):
  category = None
  if 'name' in cat:
    # Save cat
    category, created = PlaceCategory.objects.get_or_create(foursquare_id=cat['id'], defaults={'name' : cat['name']})
    print "%s %s" % (created and 'Create' or 'Update', category)
    if parent is not None:
      category.parent = parent
      category.save()

  # Recursion
  if 'categories' in cat:
    for c in cat['categories']:
      save_category(c, category)

def main():
  cache_path = 'scripts/categories.json'
  categories = cache_categories(cache_path)
  save_category(categories)

if __name__ == '__main__':
  main()
