from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsOwner(BasePermission):
    """
    Allow access only if the object's user is the same as the request user.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user