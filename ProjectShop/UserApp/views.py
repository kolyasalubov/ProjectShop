from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views, get_user_model
from django.http import JsonResponse
from django.views import generic
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from braces.views import AnonymousRequiredMixin
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from UserApp.permissions import IsAdminBot
from UserApp.forms import LoginForm, RegisterForm, EditForm

from rest_framework.viewsets import ModelViewSet
from django_filters.views import FilterView

from ProductApp.models import Review, Product, ProductCategory
# from ProductApp.serializers import ReviewSerializer
# from ProductApp.filters import ProductFilter


class LoginView(AnonymousRequiredMixin, auth_views.LoginView):
    form_class = LoginForm
    template_name = 'UserApp/login.html'


class RegisterView(AnonymousRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = RegisterForm
    template_name = 'UserApp/register.html'
    success_url = reverse_lazy('login')
    success_message = _("Congratulations! Your account has been created. You may sign in!")


class LogoutView(auth_views.LogoutView):
    template_name = 'UserApp/logout.html'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'UserApp/password_reset.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'UserApp/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'UserApp/password_reset_confirm.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'UserApp/password_reset_complete.html'


class HomePageView(ListView):
    # filterset_class = ProductFilter
    template_name = 'UserApp/home.html'
    context_object_name = 'products'
    queryset = Product.objects.all()
    # paginate_by = 12
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.order_by('name')[:20]
        context['categories'] = categories
        return context

class ProductJsonListView(View):
    def get(self, *args, **kwargs):
        print(kwargs)
        upper = kwargs.get('num_products')
        lower = upper - 4
        products = list(Product.objects.values()[lower:upper])
        products_size = len(Product.objects.all())
        max_size = True if upper >= products_size else False
        return JsonResponse({'data': products, 'max': max_size}, safe=False)


class CustomUpdateView(generic.edit.SingleObjectTemplateResponseMixin,
                       generic.edit.ModelFormMixin,
                       generic.edit.ProcessFormView):

    def get(self, request, *args, **kwargs):
        self.object = request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = request.user
        return super().post(request, *args, **kwargs)


class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, CustomUpdateView):
    form_class = EditForm
    model = get_user_model
    template_name = 'UserApp/profile.html'
    success_url = reverse_lazy('profile')
    success_message = _("Your account has been updated!")


class BlacklistRefreshViewSet(viewsets.GenericViewSet):
    """
    A simple ViewSet for creating blacklist token from refresh token.
    """
    permission_classes = (IsAdminBot, IsAuthenticated)

    def create(self, request):
        try:
            refresh_token = RefreshToken(request.data.get('refresh'))
            refresh_token.blacklist()
        except TokenError as error:
            return Response(str(error), status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_200_OK)
