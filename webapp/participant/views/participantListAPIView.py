from rest_framework.generics import CreateAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from participant.models.participant import Participant
from participant.serializers.participantSerializer import ParticipantSerializer


class ParticipantListAPIView(CreateAPIView, ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering = ['id']
    ordering_fields = ['survey', 'created_at', 'user']
