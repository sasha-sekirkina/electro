from .cart import Basket


def basket(request):
    return {'basket': Basket(request)}