from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework import serializers

from apps.communication.models import Messages, Chat

from .serializers import MessageSerializer, ChatSerializer

User = get_user_model()


class ChatViewSet(
    mixins.ListModelMixin,
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

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user, is_active=True)

    def validate_participants(self, serializer):
        participants = self.request.data.get("participants")

        if participants is None:
            raise serializers.ValidationError(
                "You should specify user with whom you want to create a chat"
            )
        if len(participants) != 1:
            raise serializers.ValidationError(
                "You should specify exactly one user with whom you want to create a chat"
            )
        if participants[0] == self.request.user.id:
            raise serializers.ValidationError("You can't create chat with yourself")
        get_object_or_404(User, id=participants[0])
        return participants + [self.request.user.id]

    def check_uniqueness_of_chat_and_create(self, serializer, participants):
        print(type(participants))
        chat = Chat.objects.filter(participants__in=participants).distinct()

        if chat.exists():
            raise serializers.ValidationError("Chat with this user already exists")
        else:
            serializer.save(participants=participants)

    def perform_create(self, serializer):
        participants = self.validate_participants(serializer)
        print(participants)
        self.check_uniqueness_of_chat_and_create(serializer, participants)


class MessageViewSet(ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
