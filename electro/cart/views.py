from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from store.models import Product
from .cart import Basket


def cart(request):
    basket = Basket(request)
    context = {
        'basket': basket,
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty })
        return response
