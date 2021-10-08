from django.urls import path

from ProductApp.views import HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
