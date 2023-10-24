from rest_framework import routers

from .views import ChatViewSet


router = routers.DefaultRouter()
router.register("chat", ChatViewSet, basename="chat")
