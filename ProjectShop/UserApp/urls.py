from django.urls import path
from UserApp.views import UserCreate


app_name = 'user_app'

urlpatterns = [
    path('register/', UserCreate.as_view(), name="user_create"),
]