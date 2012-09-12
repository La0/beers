from django import forms
from models import Product

class PriceForm(forms.Form):
  product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput)
  price = forms.IntegerField()