"""ProjectShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .router import router
from ProductApp.views import product_detail_view, category_detail_view
from order.views import MakeAnOrder, OrderConfirmation
from ProjectShop.sitemaps import (OrderSitemap,
                                  FlatPageSitemap,
                                  OrderItemsSitemap,
                                  ProductSitemap)

schema_view = get_schema_view(
    openapi.Info(
        title="Project Shop Title",
        default_version="v1",
        description="Project Shop Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mykhailo@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

sitemaps = {
    'order': OrderSitemap,
    'flatpages': FlatPageSitemap,
    'orderitems': OrderItemsSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("order/", include("order.urls")),
    path('product/', include('ProductApp.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/', include(router.urls)),
    path("users/", include("UserApp.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path('checkout/', MakeAnOrder.as_view(), name='checkout'),
    path('order-confirmation/', OrderConfirmation.as_view(), name="order-confirmation"),
    path("test/", product_detail_view),
    path('', include('ProductApp.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
