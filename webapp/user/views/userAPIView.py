from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from user.models import User
from user.serializers.userSerializer import UpdateUserSerializer


class UpdateUserAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
