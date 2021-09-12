from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from UserApp.views import UserCreate, BlacklistRefreshView


app_name = 'user_app'

urlpatterns = [
    path('register/', UserCreate.as_view(), name="user_create"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', BlacklistRefreshView.as_view(), name='token_logout'),
]