from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from apps.communication.models import Messages, Chat

from .serializers import MessageSerializer, ChatSerializer


class ChatViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ChatViewSet(ChatViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        """
        in participants can be only 2 users
        one user from request and another from url
        
        """


class MessageViewSet(ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
