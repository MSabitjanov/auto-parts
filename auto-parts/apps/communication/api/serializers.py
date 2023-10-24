from rest_framework import serializers

from apps.communication.models import Messages, Chat


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Messages
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = "__all__"