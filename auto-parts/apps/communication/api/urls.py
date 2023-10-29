from django.urls import path, include

from .routers import router

from .views import MessageListCreateAPIView, MessageUpdateAPIView

urlpatterns = [
    path("user/", include(router.urls)),
    path("user/chat/<str:chat_id>/message/", MessageListCreateAPIView.as_view(), name="message-list-create"),
    path("user/chat/<str:chat_id>/message/<int:message_id>/", MessageUpdateAPIView.as_view(), name="message-update"),
]