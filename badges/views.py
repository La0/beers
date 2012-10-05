from helpers import render
from models import *

@render('badges/index.html')
def index(request):

  return {
    'badges' : Badge.objects.all().order_by('name')
  }