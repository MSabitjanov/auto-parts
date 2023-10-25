from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

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

    def check_uniqueness_of_chat(self, serializer, participants):
        chat = Chat.objects.filter(participants=participants[0]).filter(participants=participants[1]).filter(is_active=True)

        if chat.exists():
            return chat.first().id

    def perform_create(self, serializer):
        participants = self.validate_participants(serializer)
        self.check_uniqueness_of_chat(serializer, participants)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participants = self.validate_participants(serializer)
        chat_id = self.check_uniqueness_of_chat(serializer, participants)

        if chat_id:
            return Response({"chat_id": chat_id, "message": "Chat between these users already exists."},
                            status=status.HTTP_200_OK)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MessageViewSet(ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
