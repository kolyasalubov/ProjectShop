from django.contrib import admin
from django.urls import path

from UserApp.views import UserRestView, UserRestListView

urlpatterns = [
    path('rest/<int:user_id>/', UserRestView.as_view()),
    path('rest/all', UserRestListView.as_view())
]
