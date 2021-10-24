from ProductApp.models import Product, ProductMedia


class SessionCart:
    def __init__(self, request):
        """Initialize the cart"""
        self.session = request.session
        if 'skey' not in request.session:
            self.session['skey'] = {}

        self.cart = self.session['skey']

    def count_sum_price(self, product_id):
        return float(self.cart[str(product_id)]['price']) * self.cart[str(product_id)]['qty']

    def add(self, product):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price), 'qty': 1}
        else:
            self.cart[product_id]['qty'] = self.cart[product_id]['qty'] + 1

        self.save()

        return self.cart[product_id]['qty'], self.count_sum_price(product_id)

    def substract(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] -= 1

            if self.cart[product_id]['qty'] <= 0:
                self.remove(product_id)
                self.save()
                return 0, 0
            else:
                self.save()
                return self.cart[product_id]['qty'], self.count_sum_price(product_id)

    def remove(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def save(self):
        self.session.modified = True

    def list(self):
        product_ids = self.cart.keys()
        queryset = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in queryset:
            cart[str(product.id)]['product'] = product
            cart[str(product.id)]['price'] = self.count_sum_price(product.id)
            cart[str(product.id)]['media'] = ProductMedia.objects.get(product=product)

        return cart.values()