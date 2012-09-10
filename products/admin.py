from django.contrib import admin
from models import *

class ProductAdmin(admin.ModelAdmin):
  pass
admin.site.register(Product, ProductAdmin)

class ProductCategoryAdmin(admin.ModelAdmin):
  pass
admin.site.register(ProductCategory, ProductCategoryAdmin)
