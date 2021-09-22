from django.urls import path, include
from ProductApp.api.router import router


urlpatterns = [path('', include(router.urls))
]
