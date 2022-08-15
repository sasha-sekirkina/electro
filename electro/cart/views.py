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


# def add_to_cart(request):
# basket = Basket(request)
# if request.POST.get('action') == 'post':
#     product_id = int(request.POST.get('productid'))
#     if request.POST.get('productqty'):
#         product_qty = int(request.POST.get('productqty'))
#     else:
#         product_qty = 1
#     product = get_object_or_404(Product, id=product_id)
#     basket.add(product=product, qty=product_qty)
#     basket_qty = basket.__len__()
#     response = JsonResponse({'qty': basket_qty})
#     return response


# def delete_from_cart(request):
# basket = Basket(request)
# if request.POST.get('action') == 'post':
#     product_id = int(request.POST.get('productid'))
#     basket.delete(product=product_id)
#     basket_qty = basket.__len__()
#     basket_total = basket.get_total_price()
#     response = JsonResponse({'qty': basket_qty,
#         'subtotal': basket_total,})
#     return response


# def update_cart(request):
# basket = Basket(request)
# if request.POST.get('action') == 'post':
#     product_id = int(request.POST.get('productid'))
#     product_qty = int(request.POST.get('productqty'))
#     basket.update(product=product_id, qty=product_qty)
#     basket_qty = basket.__len__()
#     basket_total = basket.get_total_price()
#     itemprice = Product.products.get(pk=product_id).price
#     item_total = itemprice * product_qty
#     response = JsonResponse({
#         'qty': basket_qty,
#         'subtotal': basket_total,
#         'prodqty': product_qty,
#         'prodtotal': item_total,
#         'productid': product_id,
#     })
#     return response


def cart_change(request):
    basket = Basket(request)
    product_id = int(request.POST.get('productid'))
    data_to_frontend = {}
    if request.POST.get('action') == 'add':
        if request.POST.get('productqty'):
            product_qty = int(request.POST.get('productqty'))
        else:
            product_qty = 1
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

    elif request.POST.get('action') == 'update':
        data_to_frontend['productid'] = product_id
        product_qty = int(request.POST.get('productqty'))
        data_to_frontend['prodqty'] = product_qty
        basket.update(product=product_id, qty=product_qty)
        basket_total = basket.get_total_price()
        data_to_frontend['subtotal'] = basket_total
        itemprice = Product.products.get(pk=product_id).price
        item_total = itemprice * product_qty
        data_to_frontend['prodtotal'] = item_total,

    elif request.POST.get('action') == 'delete':
        basket.delete(product=product_id)
        basket_total = basket.get_total_price()
        data_to_frontend['subtotal'] = basket_total

    basket_qty = basket.__len__()
    data_to_frontend['qty'] = basket_qty
    response = JsonResponse(data_to_frontend)
    return response
