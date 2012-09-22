from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^price/(?P<product_id>\w+)/place/(?P<place_id>\w+)', 'products.views.price', name="product-price"),
)
