from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from Shipping.models import ShippingModel


class AddShippingAddress(CreateView):
    """
    class for creating shipping address
    """

    model = ShippingModel
    template_name = "Shipping/add_shipping_address.html"
    fields = ["postal_code", "country", "region", "city", "post_office"]
    success_url = "/shipping/all/"


class AllShippingAddresses(ListView):
    """
    class for retrieving all shipping addresses
    """
    model = ShippingModel
    template_name = "Shipping/all_shipping_addresses.html"


class DetailShippingAddress(DetailView):
    """
    class for retrieving information for a certain shipping address (get by id)
    """

    model = ShippingModel
    template_name = "Shipping/detail_shipping_address.html"


class UpdateShippingAddress(UpdateView):
    """
    class for updating a certain shipping address
    """
    model = ShippingModel
    fields = ["postal_code", "country", "region", "city", "post_office"]
    success_url = "/shipping/all/"
    template_name = "Shipping/update_shipping_address.html"


class DeleteShippingAddress(DeleteView):
    """
    class for updating a certain shipping address
    """
    model = ShippingModel
    success_url = "/shipping/all/"
    template_name = "Shipping/delete_shipping_address.html"
