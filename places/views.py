from helpers import render
from forms import PlaceForm
from django.contrib.auth.decorators import login_required
from models import Place
from django.http import Http404, HttpResponseRedirect
from products.models import ProductPrice, ProductCategory

@render('places/index.html')
def index(request):
  
  return {
    'places' : Place.objects.all().order_by('modified'),
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
  
  prices = ProductPrice.objects.filter(place=place)
  
  return {
    'place' : place,
    'prices' : prices,
    'categories' : ProductCategory.objects.all()
  }