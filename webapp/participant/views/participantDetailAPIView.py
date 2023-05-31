from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, UpdateAPIView

from participant.models import Participant
from participant.permissions.participantPermission import ParticipantPermission
from participant.serializers.participantSerializer import ParticipantSerializer


class ParticipantDetailAPIView(RetrieveAPIView, UpdateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated, ParticipantPermission]
    lookup_url_kwarg = 'pk'
