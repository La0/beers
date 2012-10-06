from helpers import render
from forms import *
from django.contrib.auth.decorators import login_required
from models import Place, PlaceHour
from django.http import Http404, HttpResponseRedirect
from products.models import ProductPrice, ProductCategory
from geo.models import City
from django.shortcuts import get_object_or_404

@render('places/index.html')
def index(request):
  
  return {
    'places' : Place.objects.all().order_by('modified'),
    'cities' : City.objects.exclude(places=None).order_by('zipcode'),
  }

@login_required
@render('places/add.html')
def add(request):
  
  if request.method == 'POST':
    form = PlaceForm(request.POST)
    if form.is_valid():
      p = Place(name=form.cleaned_data['name'], address=form.cleaned_data['address'], city=form.cleaned_data['city'], creator=request.user)
      p.save()
      
      # Redirect to place view
      return HttpResponseRedirect(p.get_absolute_url())
  else:
    form = PlaceForm()
  
  return {
  
    'form' : form,
  }

@render('places/view.html')
def view(request, city_slug, place_slug):
  
  try:
    place = Place.objects.get(slug=place_slug, city__slug=city_slug)
  except:
    raise Http404('Place not found')
  
  prices = ProductPrice.objects.filter(place=place, current=True)
  
  return {
    'place' : place,
    'prices' : prices,
    'categories' : ProductCategory.objects.all(),
    'days' : place.get_hours_per_days(),
    'badges' : place.badges.all().order_by('name'),
  }

@render('places/city.html')
def city(request, city_slug):
  try:
    city = City.objects.get(slug=city_slug)
  except:
    raise Http404('City not found')

  return {
    'city' : city,
    'polygon' : city.get_polygon(),
    'places' : Place.objects.filter(city=city),
  }

@login_required
@render('places/hours.html')
def hours(request, place_id):
  place = get_object_or_404(Place, pk=place_id)
  
  if request.method == 'POST':
    form = PlaceHourForm(place, request.POST)
    if form.is_valid():
      for day in form.cleaned_data['day']:
        ph = PlaceHour(place=place, day=day, start=form.cleaned_data['start'], end=form.cleaned_data['end'], happy_hour=form.cleaned_data['happy_hour'])
        ph.save()
  else:
    form = PlaceHourForm(place)

  return {
    'place' : place,
    'hours' : place.hours.all().order_by('day'),
    'form' : form,
  }

@login_required
@render('places/links.html')
def links(request, place_id):
  place = get_object_or_404(Place, pk=place_id)

  link = PlaceLink(creator=request.user, place=place)
  if request.method == 'POST':
    form = PlaceLinkForm(request.POST, instance=link)
    if form.is_valid():
      if not form.instance.search_title():
        form.instance.title = 'Link from %s' % form.instance.get_domain()
      form.save()
  else:
    form = PlaceLinkForm(instance=link)

  return {
    'place' : place,
    'form'  : form,
    'links' : place.links.all(),
  }