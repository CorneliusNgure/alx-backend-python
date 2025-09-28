from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access messages within that conversation.
    """

    def has_permission(self, request, view):
        # authenticated user
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user is a participant
        in the conversation related to the object.
        """

        if isinstance(obj, Message):
            # For a message, check if the user is the sender or recipient
            return (
                obj.sender == request.user
                or obj.recipient == request.user
            )

        if isinstance(obj, Conversation):
            # For a conversation, check if the user is among participants
            return request.user in obj.participants.all()

        return False
