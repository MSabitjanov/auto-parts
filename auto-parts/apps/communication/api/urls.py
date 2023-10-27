from django.urls import path, include

from .routers import router

from .views import MessageListCreateAPIView

urlpatterns = [
    path("user/", include(router.urls)),
    path("user/chat/<int:pk>/message/", MessageListCreateAPIView.as_view(), name="message-list"),
    path("user/chat/<int:pk>/message/", MessageListCreateAPIView.as_view(), name="message-create"),
]