from rest_framework import serializers

from apps.communication.models import Messages, Chat
from apps.users.api.serializers import UserSerializerForChat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = "__all__"
        read_only_fields = "sender", "chat",

    def update(self, instance, validated_data):
        instance.is_read = validated_data.get("is_read", instance.is_read)
        instance.save()
        return instance

class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializerForChat(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = "__all__"
        read_only_fields = ("last_message_received_time", "id", "is_active")
        extra_kwargs = {
            "participants": {
                "help_text": "User with whom you want to create a chat",
            }
        }
