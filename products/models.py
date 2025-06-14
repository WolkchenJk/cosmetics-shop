from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    show_in_menu = models.BooleanField(default=True) 
    
    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name

class Product(models.Model):
    category    = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name        = models.CharField(max_length=200)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name        = models.CharField(max_length=200)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    stock       = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image   = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.product.name} — изображение"
    
    

