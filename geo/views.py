from helpers import render
from geo.models import SubwayLine
from places.models import City, Place
from django.shortcuts import get_object_or_404
from geo.geocoding import AddressFinder
import geojson

@render('geo/subway.html')
def subway(request):
  
  lines = SubwayLine.objects.all().order_by('name')
  
  return {
    'lines' : lines,
  }

@render('geo/city.html')
def city(request, city_id):
  city = get_object_or_404(City, pk=city_id)
  
  if request.method == 'POST':
    print request.POST
  
  return {
    'city': city,
  }

@render('geo/place.html')
def place(request, place_id):
  place = get_object_or_404(Place, pk=place_id)

  # Save position
  if request.method == 'POST':
    p = geojson.Point([request.POST['lat'], request.POST['lng']])
    place.geojson = geojson.dumps(p)
    place.find_subways() # Update subways
    place.find_city() # Update city
    place.save()

  # Find address
  af = AddressFinder(place.address, place.city)
  res = af.search()

  return {
    'place' : place,
    'results' : res,
    'point' : place.get_point(),
  }