from django.contrib import admin
from models import *

class PlaceAdmin(admin.ModelAdmin):
  pass
admin.site.register(Place, PlaceAdmin)
