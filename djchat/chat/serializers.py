from chat.models import ChatMessage
from rest_framework import serializers


class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    post_time = serializers.DateTimeField(format="%d.%m.%y %H:%M")

    class Meta:
        model = ChatMessage
        fields = ["username", "message", "post_time"]
