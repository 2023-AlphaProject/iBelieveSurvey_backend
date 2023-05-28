from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from participant.models.participant import Participant
from participant.permissions.participantPermission import WriterPermission
from participant.serializers.participantSerializer import ParticipantSerializer


class ParticipantListAPIView(ListAPIView):
    queryset = Participant.objects.all()
    permission_classes = [IsAuthenticated, WriterPermission]
    serializer_class = ParticipantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering = ['id']
    ordering_fields = ['survey', 'created_at', 'user']
