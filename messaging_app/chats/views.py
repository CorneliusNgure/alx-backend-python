"""
Views for the chats app.

Provides API endpoints for managing conversations and messages.
"""

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsParticipantOfConversation
from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer
from .filters import MessageFilter
from .pagination import MessagePagination


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing conversations.

    - List all conversations for the authenticated user
    - Create a new conversation with selected participants
    """

    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__email"]

    def get_queryset(self):
        """
        Restrict conversations to those involving the current user.
        """
        return Conversation.objects.filter(
            participants=self.request.user
        ).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with given participants.
        """
        participant_ids = request.data.get("participants", [])

        if not participant_ids:
            return Response(
                {"error": "Participants are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure the authenticated user is included
        participant_ids.append(str(request.user.user_id))
        participants = CustomUser.objects.filter(user_id__in=participant_ids)

        if participants.count() < 2:
            return Response(
                {"error": "A conversation requires at least 2 participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing messages.

    - List all messages in a conversation
    - Send a new message in a conversation
    """

    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    pagination_class = MessagePagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["message_body"]
    filterset_class = MessageFilter

    def get_queryset(self):
        """
        Retrieve messages belonging to a specific conversation.
        """
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(
            Conversation,
            conversation_id=conversation_id,
            participants=self.request.user,
        )
        return Message.objects.filter(
            sender__in=conversation.participants.all(),
            recipient__in=conversation.participants.all(),
        ).order_by("sent_at")

    def create(self, request, *args, **kwargs):
        """
        Send a message to a participant in the conversation.
        """
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(
            Conversation,
            conversation_id=conversation_id,
            participants=request.user,
        )

        recipient_id = request.data.get("recipient")
        message_body = request.data.get("message_body")

        if not recipient_id or not message_body:
            return Response(
                {"error": "Recipient and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recipient = get_object_or_404(CustomUser, user_id=recipient_id)

        if recipient not in conversation.participants.all():
            return Response(
                {"error": "Recipient must be part of the conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            message_body=message_body,
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
