from helpers import render
from geo.models import SubwayLine
from places.models import City
from django.shortcuts import get_object_or_404

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