from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from participant.models import Participant
from participant.permissions.participantPermission import ParticipantPermission
from participant.permissions.writerPermission import WriterPermission
from participant.serializers.participantSerializer import ParticipantSerializer


class JsonQualityStandardOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            # Check if the first ordering field is 'json_quality_standard'
            if ordering[0] == 'json_quality_standard':
                is_descending = ordering[0].startswith('-')
                return sorted(queryset, key=lambda p: p.json_quality_standard, reverse=is_descending)

        return queryset


class ParticipantListAPIView(ListAPIView):
    serializer_class = ParticipantSerializer
    ordering = ['id']
    queryset = Participant.objects.all()
    filter_backends = [JsonQualityStandardOrderingFilter]
    permission_classes = [IsAuthenticated, WriterPermission]
    ordering_fields = ['json_quality_standard']

    def get_queryset(self):
        survey_id = self.kwargs['survey_id']
        queryset = Participant.objects.filter(survey_id=survey_id).order_by('id')

        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), ParticipantPermission()]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
