from django.contrib.auth import views as auth_views
from django.urls import path

from UserApp.views import LoginView, RegisterView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='UserApp/logout.html'), name='logout'),
]
