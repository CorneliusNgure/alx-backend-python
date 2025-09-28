from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated participants
    of a conversation to send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user is a participant
        in the conversation related to the object.
        """

        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            if isinstance(obj, Message):
                # For messages: sender or recipient must be the request user
                return (
                    obj.sender == request.user
                    or obj.recipient == request.user
                )

            if isinstance(obj, Conversation):
                # For conversations: user must be among participants
                return request.user in obj.participants.all()

        return False
