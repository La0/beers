from django.contrib import admin
from geo.models import *

class SubwayLineAdmin(admin.ModelAdmin):
  pass
admin.site.register(SubwayLine, SubwayLineAdmin)

class CityAdmin(admin.ModelAdmin):
  pass
admin.site.register(City, CityAdmin)