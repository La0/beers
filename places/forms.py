from django import forms
from models import *
from geo.models import City

class PlaceForm(forms.Form):
  type = forms.ChoiceField(choices=PLACE_TYPE)
  name = forms.CharField()
  address = forms.CharField()
  city = forms.ModelChoiceField(queryset=City.objects.all())

class PlaceHourForm(forms.Form):
  _place = None
  day = forms.MultipleChoiceField(choices=WEEK_DAYS, widget=forms.CheckboxSelectMultiple)
  start = forms.TimeField()
  end = forms.TimeField()
  happy_hour = forms.BooleanField(required=False)
  
  def __init__(self, place, *args, **kwargs):
    self._place = place
    super(forms.Form, self).__init__(*args, **kwargs)
  
  def clean_day(self):
    if 'day' not in self.cleaned_data:
      return []
    return [int(d) for d in self.cleaned_data['day']]
  
  def clean(self):
    if 'day' not in self.cleaned_data:
      return self.cleaned_data

    for day in self.cleaned_data['day']:
      print 'Day %d' % (day)
      hour = None
      try:
        hour = self._place.hours.get(day=day, happy_hour=self.cleaned_data['happy_hour'])
      except:
        continue # no hour conflict, go on...
      raise forms.ValidationError('You can\'t add another hour on day #%d.' % day)
    
    return self.cleaned_data

class PlaceLinkForm(forms.ModelForm):
  class Meta:
    model = PlaceLink
    exclude = ('place', 'creator', 'title')

  def clean(self):
    try:
      PlaceLink.objects.get(place=self.instance.place, url=self.cleaned_data['url'])
    except:
      return self.cleaned_data
    raise forms.ValidationError('This link already exist for this place')