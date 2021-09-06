from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)

from .models import ShippingModel
from .forms import ShippingForm


def add_shipping_address(request):
    context = {}

    form = ShippingForm(request.POST or None)
    if form.is_valid():
        form.save()

    context['form'] = form
    return render(request, "add_shipping_address.html", context)


def all_shipping_addresses(request):
    context = {"dataset": ShippingModel.objects.all()}
    return render(request, "all_shipping_addresses.html", context)


def detail_shipping_address(request, id):
    context = {"data": ShippingModel.objects.get(id=id)}
    return render(request, "detail_shipping_address.html", context)


def update_shipping_address(request, id):
    context = {}

    obj = get_object_or_404(ShippingModel, id=id)

    form = ShippingForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/shipping/" + id)

    context["form"] = form

    return render(request, "update_shipping_address.html", context)


def delete_shipping_address(request, id):
    context = {}

    obj = get_object_or_404(ShippingModel, id=id)

    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/shipping/all/")

    return render(request, "delete_shipping_address.html", context)
