from rest_framework import routers

from .views import MasterViewSet, SellerViewSet

router = routers.DefaultRouter()

router.register("master", MasterViewSet, basename="master")
router.register("seller", SellerViewSet, basename="seller")
