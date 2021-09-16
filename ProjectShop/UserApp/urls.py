from django.urls import path
from django.contrib.auth import views as auth_views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from UserApp.views import BlacklistRefreshViewSet, LoginView, RegisterView

app_name = 'user_app'

view_based_urls = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='UserApp/logout.html'), name='logout'),
]

token_urls = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # it is default View for token auth.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # it is default View for token auth.
]

router = DefaultRouter()
router.register(r'token/logout', BlacklistRefreshViewSet, basename='user')
urlpatterns = router.urls + token_urls + view_based_urls
