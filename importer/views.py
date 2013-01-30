from helpers import render
from importer.models import *

@render('importer/categories.html')
def categories(request):
  categories = PlaceCategory.objects.all().order_by('name')

  if request.method == 'POST':
    active = request.POST.getlist('category')

    # Set inactive
    for cat in categories.filter(used=True).exclude(id__in=active):
      cat.used = False
      cat.save()

    # Set active
    for cat in categories.filter(id__in=active):
      cat.used = True
      for child in cat.get_all_children():
        child.used = True
        child.save()
      cat.save()

  return {
    'all_categories' : categories,
    'categories' : categories.filter(parent=None),
  }
