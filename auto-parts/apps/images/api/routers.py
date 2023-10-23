from rest_framework import routers

from .views import MasterImagesViewSet, AutoPartsImagesViewSet

router = routers.DefaultRouter()
router.register("master-image", MasterImagesViewSet, basename="master_image")
router.register("auto-part-image", AutoPartsImagesViewSet, basename="part_image")
