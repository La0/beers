from helpers import render
from importer.models import *

@render('importer/categories.html')
def categories(request):
  print 'plop'
  return {
    'plop' : 42, 
  }
