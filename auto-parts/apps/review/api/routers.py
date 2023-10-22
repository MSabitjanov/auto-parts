from rest_framework import routers

from .views import MasterReviewViewSet, AutoPartsReviewViewSet

router = routers.DefaultRouter()
router.register("review/master", MasterReviewViewSet, basename="review_master")
router.register(
    "review/auto-part", AutoPartsReviewViewSet, basename="review_auto_parts"
)
