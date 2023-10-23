from rest_framework import routers

from .views import AutoPartViewSet

router = routers.DefaultRouter()
router.register("auto-part", AutoPartViewSet, basename="auto-parts")
