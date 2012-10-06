from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^/?$', 'badges.views.index', name="badges"),
    url(r'^add/(?P<place_id>\d+)$', 'badges.views.add', name="badge-add"),        
)
