from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from bars.settings import MEDIA_ROOT

urlpatterns = patterns('',
    url(r'^geo/', include('geo.urls')),
    url(r'^places/', include('places.urls')),

    # User
    (r'^login$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}),
    (r'^logout$', 'django.contrib.auth.views.logout', {'template_name': 'users/logout.html'}),

    # Medias for dev
    (r'^medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'places.views.index'),
)
