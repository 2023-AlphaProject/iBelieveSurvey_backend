from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from user.models import User
from user.serializers.userSerializer import UpdateUserSerializer


class UpdateUserAPIView(RetrieveUpdateAPIView):
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
