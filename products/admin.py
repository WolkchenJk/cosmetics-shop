from django.contrib import admin
from django import forms
from .models import Category, Product, ProductImage

# Inline-класс для изображений товаров
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2

# Форма для Product с динамическим убиранием поля price для категории "aromati"
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # скрываем поле price, если редактируемый товар в категории с slug='aromati'
        if self.instance and self.instance.pk and self.instance.category.slug == 'aromati':
            self.fields.pop('price', None)

# Админка для категорий
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'show_in_menu')
    list_editable = ('show_in_menu',)

# Админка для товаров
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = [ProductImageInline]
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category',)

    class Media:
        js = ('js/admin-hide-price.js',)



