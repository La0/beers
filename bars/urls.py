from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from bars.settings import MEDIA_ROOT

urlpatterns = patterns('',
    url(r'^geo/', include('geo.urls')),
    url(r'^places/', include('places.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^product/', include('products.urls')),
    url(r'^badge/', include('badges.urls')),

    # Medias for dev
    (r'^medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'places.views.index'),
)
