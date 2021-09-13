from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import ShippingModel


class AddShippingAddress(CreateView):
    """
    class for creating shipping address
    """

    model = ShippingModel
    template_name = "D:/Python/Internship/OnlineShop/ProjectShop/ProjectShop/Shipping/templates/add_shipping_address.html"
    fields = ["postal_code", "country", "region", "city", "post_office"]


class AllShippingAddresses(ListView):
    """
    class for retrieving all shipping addresses
    """
    model = ShippingModel
    template_name = "D:/Python/Internship/OnlineShop/ProjectShop/ProjectShop/Shipping/templates/all_shipping_addresses.html"


class DetailShippingAddress(DetailView):
    """
    class for retrieving information for a certain shipping address (get by id)
    """

    model = ShippingModel
    template_name = "D:/Python/Internship/OnlineShop/ProjectShop/ProjectShop/Shipping/templates/detail_shipping_address.html"


class UpdateShippingAddress(UpdateView):
    """
    class for updating a certain shipping address
    """
    model = ShippingModel
    fields = ["postal_code", "country", "region", "city", "post_office"]
    success_url = "/shipping/all/"
    template_name = "D:/Python/Internship/OnlineShop/ProjectShop/ProjectShop/Shipping/templates/update_shipping_address.html"


class DeleteShippingAddress(DeleteView):
    """
    class for updating a certain shipping address
    """
    model = ShippingModel
    success_url = "/shipping/all/"
    template_name = "D:/Python/Internship/OnlineShop/ProjectShop/ProjectShop/Shipping/templates/delete_shipping_address.html"
