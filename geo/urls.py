from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^subway/?$', 'geo.views.subway', name="subway"),
    url(r'^city/(?P<city_id>(\d+))?$', 'geo.views.city', name="city"),
    url(r'^place/(?P<place_id>(\d+))?$', 'geo.views.place', name="place-map"),
)
