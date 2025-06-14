import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category

class DlyaTelaView(ListView):
    model = Product
    template_name = 'products/dlya_tela.html'
    context_object_name = 'products'
    paginate_by = 12
    def get_queryset(self):
        return Product.objects.filter(category__slug='dlya-tela')

class DlyaVolosView(ListView):
    model = Product
    template_name = 'products/dlya_volos.html'
    context_object_name = 'products'
    paginate_by = 12
    def get_queryset(self):
        return Product.objects.filter(category__slug='dlya-volos')
    
class AromatiView(ListView):
    model = Product
    template_name = 'products/aromati.html'
    context_object_name = 'products'
    paginate_by = 12
    def get_queryset(self):
        return Product.objects.filter(category__slug='aromati')

class ParfumView(ListView):
    model = Product
    template_name = 'products/parfum.html'
    context_object_name = 'products'
    paginate_by = 12
    def get_queryset(self):
        return Product.objects.filter(category__slug='parfum')


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12 

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
class AboutView(TemplateView):
    template_name = 'products/about.html'


@require_POST
@csrf_exempt  
def cart_add(request):
    data = json.loads(request.body)
    pid = str(data.get('product_id'))
    qty = int(data.get('quantity', 1))
    cart = request.session.get('cart', {})
    new_qty = cart.get(pid, 0) + qty
    if new_qty <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = new_qty
    request.session['cart'] = cart
    return JsonResponse({'cart': cart})

@require_POST
@csrf_exempt
def cart_remove(request):
    data = json.loads(request.body)
    pid = str(data.get('product_id'))
    cart = request.session.get('cart', {})
    if pid in cart:
        del cart[pid]
        request.session['cart'] = cart
    return JsonResponse({'cart': cart})

def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        prod = get_object_or_404(Product, pk=pid)
        subtotal = prod.price * qty
        image_url = ''
        img = prod.images.first()
        if img:
            image_url = img.image.url
        items.append({
            'id': prod.pk,
            'name': prod.name,
            'price': float(prod.price),
            'quantity': qty,
            'subtotal': float(subtotal),
            'image': image_url,
        })
        total += subtotal
    return JsonResponse({'items': items, 'total': float(total)})

class CartView(TemplateView):
    template_name = 'products/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        items = []
        total = 0
        for pid, qty in cart.items():
            prod = get_object_or_404(Product, pk=pid)
            subtotal = prod.price * qty
            items.append({
                'product': prod,
                'quantity': qty,
                'subtotal': subtotal,
            })
            total += subtotal
        context['cart_items'] = items
        context['cart_total'] = total
        return context


class CategoryProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])
 
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = Category.objects.get(slug=self.kwargs['slug'])
        return ctx





