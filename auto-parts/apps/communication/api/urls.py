from django.urls import path, include

from .routers import router

urlpatterns = [
    path("user/", include(router.urls)),
]