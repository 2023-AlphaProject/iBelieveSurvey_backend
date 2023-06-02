from rest_framework import permissions


class IsSurveyOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            if obj.is_survey_hidden and obj.is_end:
                return obj.writer == request.user
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user
        return obj.writer == request.user
