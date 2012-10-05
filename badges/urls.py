from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^/?$', 'badges.views.index', name="badges"),    
)
