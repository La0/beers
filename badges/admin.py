from django.contrib import admin
from models import *

class BadgeAdmin(admin.ModelAdmin):
  pass
admin.site.register(Badge, BadgeAdmin)
