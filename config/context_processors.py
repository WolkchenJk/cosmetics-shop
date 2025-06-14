# config/context_processors.py
from products.models import Category

def menu_categories(request):
    return {'menu_categories': Category.objects.filter(show_in_menu=True)}
