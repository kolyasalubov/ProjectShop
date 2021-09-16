from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from UserApp.views import UserCreate, BlacklistRefreshViewSet


app_name = 'user_app'

view_based_urls = [
    path('register/', UserCreate.as_view(), name="user_create"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # it is default View for token auth.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # it is default View for token auth.
]

router = DefaultRouter()
router.register(r'token/logout', BlacklistRefreshViewSet, basename='user')
urlpatterns = router.urls + view_based_urls
