# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime

# Setup django
sys.path.append(os.path.realpath('.'))
from django.core.management import setup_environ
import bars.settings
setup_environ(bars.settings)

# Models
from products.models import ProductCategory, Product
from django.contrib.auth.models import User

# Tools
from urllib2 import urlopen
import simplejson as json

# Load user & category
# TODO: use conf or param
owner = User.objects.get(pk=1)
category = ProductCategory.objects.get(slug='beer')

# Load beers
source = 'scripts/beers.txt'
fd = open(source, 'r')
beers = fd.read().split('\n')
fd.close()

# Search for the wikipedia link
wikipedia_search = 'http://fr.wikipedia.org/w/api.php?action=opensearch&search=%s'
wikipedia_article = 'http://fr.wikipedia.org/wiki/%s'
for beer in beers:
  print "Beer: %s" % beer

  page_url = None
  results = None
  try:
    fd = urlopen(wikipedia_search % beer.replace(' ', '+'))
    _, results = json.loads(fd.read())
    if not len(results):
      raise Exception('No results')
  except Exception, e:
    print 'Woops: %s' % (str(e),)

  # Select page
  if results:
    page = results[0]
    filtered = [r for r in results if u'bi\xe8re' in r]
    page = len(filtered) == 1 and filtered[0] or results[0]
    page_url = wikipedia_article % page.replace(' ', '_')
  
  # Add beer
  try:
    b = Product(name=beer, category=category, creator=owner)
    if page_url is not None:
      b.wikipedia = page_url
    b.save()
    print 'Created beer #%d %s ' % (b.id, b.slug)
  except Exception, e:
    print 'Already exist : %s' % (str(e),)
  
  print 20*'-'