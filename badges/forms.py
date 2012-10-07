from django import forms
from models import Badge

class BadgeForm(forms.Form):
  badge = forms.ModelChoiceField(queryset=Badge.objects.all())
  
  def __init__(self, place, *args, **kwargs):
    super(forms.Form, self).__init__(*args, **kwargs)
    
    # Update queryset to exclude used badges
    badges = Badge.objects.exclude(pk__in=place.badges.all()).order_by('name')
    setattr(self.fields['badge'], 'queryset', badges)
