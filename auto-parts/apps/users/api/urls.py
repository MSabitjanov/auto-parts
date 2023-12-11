from django.urls import path, include
from rest_framework.authtoken import views

from .views import (
    MasterListAPIView,
    UserViewSet,
    MasterSkillListAPIView,
    MasterBySkillListAPIView,
    RegionListAPIView,
    CustomObtainAuthToken,
    MasterSkillListAllAPIView,
)
from .routers import router

urlpatterns = [
    path("", include(router.urls)),
    path("masters/", MasterListAPIView.as_view(), name="master-list"),
    path("user/<int:pk>/", UserViewSet.as_view()),
    path(
        "master/skill/<int:skill_id>/",
        MasterBySkillListAPIView.as_view(),
        name="master-by-skill-list",
    ),
    path("master-skills/", MasterSkillListAPIView.as_view(), name="master-skills-list"),
    path("master-skills-all/", MasterSkillListAllAPIView.as_view(), name="master-skills-list-all"),
    path("regions/", RegionListAPIView.as_view(), name="regions-list"),
    path("user/api-token-auth/", CustomObtainAuthToken.as_view()),
]
