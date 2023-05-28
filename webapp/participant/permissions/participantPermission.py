from rest_framework import permissions


class WriterPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return obj.survey.writer == request.user
        return False
