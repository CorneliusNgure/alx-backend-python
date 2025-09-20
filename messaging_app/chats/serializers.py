"""
Serializers for the chats app.

Handles serialization for CustomUser, Conversation, and Message models.
Supports nested relationships such as embedding messages within a
conversation.
"""

from rest_framework import serializers
from django.conf import settings
from .models import CustomUser, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.

    Adds custom validation for email to demonstrate usage of
    serializers.CharField and serializers.ValidationError.
    """

    email = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = [
            "user_id",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = ["user_id", "created_at"]

    def validate_email(self, value):
        """
        Ensure email is not empty and contains '@'.
        """
        if not value or "@" not in value:
            raise serializers.ValidationError(
                "A valid email address is required."
            )
        return value


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.

    Includes sender and recipient details via nested UserSerializer.
    """

    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "recipient",
            "message_body",
            "sent_at",
        ]
        read_only_fields = ["message_id", "sent_at"]

    def validate_message_body(self, value):
        """
        Ensure message body is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError(
                "Message body cannot be empty."
            )
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.

    Includes participants as nested users and messages related to this
    conversation.
    """

    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
        ]
        read_only_fields = ["conversation_id", "created_at"]

    def get_messages(self, obj):
        """
        Return all messages linked to this conversation.
        """
        participants = obj.participants.all()
        messages = Message.objects.filter(
            sender__in=participants,
            recipient__in=participants
        ).order_by("sent_at")
        return MessageSerializer(messages, many=True).data

