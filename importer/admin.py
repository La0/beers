from django.contrib import admin
from importer.models import *

class PlaceCategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'parent')
admin.site.register(PlaceCategory, PlaceCategoryAdmin)
