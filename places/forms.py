from django import forms
from models import PLACE_TYPE
from geo.models import City

class PlaceForm(forms.Form):
  type = forms.ChoiceField(choices=PLACE_TYPE)
  name = forms.CharField()
  address = forms.CharField()
  city = forms.ModelChoiceField(queryset=City.objects.all())