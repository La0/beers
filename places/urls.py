from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^/?$', 'places.views.index', name="places"),
    url(r'^add$', 'places.views.add', name="place-add"),
    
    # Place edit
    url(r'^(?P<place_id>\d+)/hours$', 'places.views.hours', name="place-hours"),

    url(r'^(?P<city_slug>\w+)/(?P<place_slug>\w+)', 'places.views.view', name="place-view"),
    url(r'^(?P<city_slug>\w+)/?$', 'places.views.city', name="city-view"),

)
