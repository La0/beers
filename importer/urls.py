from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^categories/?$', 'importer.views.categories', name="importer-categories"),
)
