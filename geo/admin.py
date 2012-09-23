from django.contrib import admin
from geo.models import *

class SubwayLineAdmin(admin.ModelAdmin):
  pass
admin.site.register(SubwayLine, SubwayLineAdmin)

class SubwayStationAdmin(admin.ModelAdmin):
  list_filter = ('lines',)
admin.site.register(SubwayStation, SubwayStationAdmin)

class CityAdmin(admin.ModelAdmin):
  pass
admin.site.register(City, CityAdmin)