from django import forms
from models import Badge

class BadgeForm(forms.Form):
  badge = forms.ModelChoiceField(queryset=Badge.objects.all())
  
  def __init__(self, place, *args, **kwargs):
    super(forms.Form, self).__init__(*args, **kwargs)
    
    # Update queryset to exclude used badges
    used = place.badges.values('pk')
    badges = Badge.objects.all().order_by('name').exclude(pk=used)
    self['badge'].queryset = badges
