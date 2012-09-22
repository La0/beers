from helpers import render
from django.shortcuts import get_object_or_404
from models import Product, ProductPrice
from places.models import Place
from forms import PriceForm
from django.contrib.auth.decorators import login_required

@login_required
@render('products/price.html')
def price(request, product_id, place_id):
  '''
  Add a price for a product
  '''
  product = get_object_or_404(Product, pk=product_id)
  place = get_object_or_404(Place, pk=place_id)

  # Prices
  prices = ProductPrice.objects.filter(product=product, place=place).order_by('-created')
  price_current = len(prices) > 0 and prices.get(current=True) or None

  # Form
  add_price = ProductPrice(creator=request.user, product=product, place=place, current=True)
  if request.method == 'POST':
    form = PriceForm(request.POST, instance=add_price)
    if form.is_valid():
      # Unset older current price
      if price_current is not None:
        price_current.current = False
        price_current.save()

      # Save current price
      price_current = form.save()
      prices.update()

      form.cleaned_data['price'] = None
  else:
    form = PriceForm(instance=add_price)

  return {
    'product' : product,
    'place'   : place,
    'prices'  : prices,
    'price_current' : price_current,
    'form'    : form,
  }