from django.urls import path, include
from rest_framework.authtoken import views

from .views import (
    UserViewSet,
    MasterSkillListAPIView,
    RegionListAPIView,
    CustomObtainAuthToken,
)
from .routers import router

urlpatterns = [
    path("", include(router.urls)),
    path("user/<int:pk>/", UserViewSet.as_view()),
    path("master-skills/", MasterSkillListAPIView.as_view(), name="master-skills-list"),
    path("regions/", RegionListAPIView.as_view(), name="regions-list"),
    path("user/api-token-auth/", CustomObtainAuthToken.as_view()),
]
