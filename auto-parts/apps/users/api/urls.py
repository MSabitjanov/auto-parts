from django.urls import path, include

from .views import UserViewSet
from .routers import router

urlpatterns = [
    # path('', include(router.urls)),
    path('user/<int:pk>/', UserViewSet.as_view()),
]