from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User
from user.serializers.UserSerializer import UpdateUserSerializer,UserViewSerializer

class UpdateUserAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

