from rest_framework import permissions


class ParticipantPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ["GET", "POST", "PUT"]:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "POST", "PUT"]:
            return obj.user == request.user
        return False
