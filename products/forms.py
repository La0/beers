from django import forms
from models import ProductPrice
from datetime import datetime, timedelta

class PriceForm(forms.ModelForm):
  class Meta:
    model = ProductPrice
    exclude = ('product', 'place', 'creator', 'current')

  def clean(self):
    # Check a price has not already been set today by this user
    limit = datetime.now() - timedelta(days=1)
    existing = ProductPrice.objects.filter(place=self.instance.place, product=self.instance.product, creator=self.instance.creator, created__gt=limit)
    if existing.exists():
      raise forms.ValidationError('You already set a price for this product today')

    return self.cleaned_data