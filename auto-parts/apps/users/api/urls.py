from django.urls import path, include

from .views import (
    UserViewSet,
    MasterSkillListAPIView,
    RegionListAPIView,
)
from .routers import router

urlpatterns = [
    path("", include(router.urls)),
    path("user/<int:pk>/", UserViewSet.as_view()),
    path("master-skills/", MasterSkillListAPIView.as_view(), name="master-skills-list"),
    path("regions/", RegionListAPIView.as_view(), name="regions-list"),
]
