from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from UserApp.views import (
    BlacklistRefreshViewSet,
    LoginView,
    RegisterView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    UpdateProfileView,
    PasswordChangeView,
)

view_based_urls = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", UpdateProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-change/", PasswordChangeView.as_view(), name="password_change"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
token_urls = [
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # it is default View for token auth.
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # it is default View for token auth.
]

router = DefaultRouter()
router.register(r'token/logout', BlacklistRefreshViewSet, basename='users')

urlpatterns = router.urls + token_urls + view_based_urls
