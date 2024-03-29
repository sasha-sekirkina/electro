from store.models import Product


class Basket():
    """
    A base Basket class, providing some default behaviors
    that can be inherited or overwritten, as necessary
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in self.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def save(self):
        self.session.modified = True

    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price),
                                       'qty': int(qty),
                                       }
        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['total_price'] = int(item['price']) * int(item['qty'])
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty
        """
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(int(item['price']) * int(item['qty']) for item in self.basket.values())

    def delete(self, product):
        """
        Delete item from session data.
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product, qty):
        """
        Updating the users basket session data
        """
        product_id = str(product)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
            self.save()
