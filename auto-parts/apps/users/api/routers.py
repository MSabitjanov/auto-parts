from rest_framework import routers

from .views import MasterViewSet

router = routers.DefaultRouter()

router.register("master", MasterViewSet, basename="master")
