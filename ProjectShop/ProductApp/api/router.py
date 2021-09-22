from rest_framework import routers
from ProductApp.api.views import ReviewViewSet

router = routers.DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename="replies")
