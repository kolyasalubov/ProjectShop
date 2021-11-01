from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.contrib.flatpages.models import FlatPage

from order.models import Order, OrderItems


class FlatPageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return FlatPage.objects.all()


class OrderSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Order.objects.all()

    def lastmod(self, obj):
        return obj.order_date

    def location(self, obj):
        return f'/api/v1/order/{obj.pk}'

class OrderItemsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Order.objects.all()

    def lastmod(self, obj):
        return obj.order_date

    def location(self, obj):
        return f'/api/v1/orderitems/{obj.pk}'