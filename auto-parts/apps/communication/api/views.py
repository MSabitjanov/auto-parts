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


class MessageViewSet(ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
