from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from apps.communication.models import Messages, Chat
from apps.core.api.api_permissions import IsChatParticipant

from .serializers import MessageSerializer, ChatSerializer

User = get_user_model()


class ChatViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    # mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ChatViewSet(ChatViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user, is_active=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.perform_soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participants = self.validate_participants(serializer)
        chat = self.check_uniqueness_of_chat(serializer, participants)

        if chat:
            return Response(
                {
                    "chat_id": chat,
                    "message": "Chat between these users already exists.",
                },
                status=status.HTTP_200_OK,
            )

        self.perform_create(serializer, participants)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def validate_participants(self, serializer):
        """Check if participants are specified and if they are valid"""

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
        user = get_object_or_404(User, id=participants[0])
        if not user.is_active:
            raise serializers.ValidationError(
                "You can not create chat with user, since user is deleted or banned"
            )
        return participants + [self.request.user.id]

    def check_uniqueness_of_chat(self, serializer, participants: list):
        """
        Check if chat between these users already exists
        If it exists - return chat id
        """
        chat = (
            Chat.objects.filter(participants=participants[0])
            .filter(participants=participants[1])
            .filter(is_active=True)
        )

        if chat.exists():
            return chat.first().id

    def perform_create(self, serializer, participants):
        serializer.save(participants=participants)

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class MessageListCreateAPIView(ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    lookup_field = "chat_id"
    permission_classes = [IsAuthenticated, IsChatParticipant]

    def get_queryset(self):
        chat = self.validate_and_get_chat()
        return super().get_queryset().filter(chat=chat)

    def perform_create(self, serializer):
        chat = self.validate_and_get_chat()
        serializer.save(sender=self.request.user, chat=chat)

    def validate_and_get_chat(self):
        chat_id = self.kwargs.get("chat_id")
        chat = get_object_or_404(Chat.objects.all(), id=chat_id)
        return chat
    

class MessageUpdateAPIView(UpdateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    lookup_field = "message_id"
    permission_classes = [IsAuthenticated, IsChatParticipant]

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {
            'chat__id': self.kwargs.get('chat_id'),
            'id': self.kwargs.get('message_id')
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj