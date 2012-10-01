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
  happy_hour = forms.BooleanField()
  
  def __init__(self, place, *args, **kwargs):
    self._place = place
    super(forms.Form, self).__init__(*args, **kwargs)
  
  def clean_day(self):
    return [int(d) for d in self.cleaned_data['day']]
  
  def clean(self):
    for day in self.cleaned_data['day']:
      print 'Day %d' % (day)
      hour = None
      try:
        hour = self._place.hours.get(day=day, happy_hour=self.cleaned_data['happy_hour'])
      except:
        continue # no hour conflict, go on...
      raise forms.ValidationError('You can\'t add another hour on day #%d.' % day)
    
    return self.cleaned_data