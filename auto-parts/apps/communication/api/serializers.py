from rest_framework import serializers

from apps.communication.models import Messages, Chat
from apps.users.api.serializers import UserSerializerForChat

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializerForChat(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = "__all__"
        read_only_fields = ("last_message_received_time", "id")
        extra_kwargs = {
            "user": {"help_text": "User with whom you want to create a chat"}
        }
