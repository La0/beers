from helpers import render
from models import *
from forms import *
from places.models import Place
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@render('badges/index.html')
def index(request):

  return {
    'badges' : Badge.objects.all().order_by('name')
  }

@render('badges/view.html')
def view(request, badge_slug):
  badge = get_object_or_404(Badge,slug=badge_slug)
  return {
    'badge' : badge,
    'places_badges' : badge.places.all(),
  }

@login_required
@render('badges/add.html')
def add(request, place_id):
  place = get_object_or_404(Place, pk=place_id)

  if request.method == 'POST':
    form = BadgeForm(place, request.POST)
    if form.is_valid():
      pb = PlaceBadge(place=place, badge=form.cleaned_data['badge'], user=request.user)
      pb.save()
  else:
    form = BadgeForm(place)

  return {
    'place'   : place,
    'form'    : form,
    'badges'  : place.badges.all().order_by('name'),
  }