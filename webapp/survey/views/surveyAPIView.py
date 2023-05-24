from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView

from survey.models import Survey
from survey.serializers import SurveySerializer


class SurveyAPIView(CreateAPIView, ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering = ['id']
    ordering_fields = ['started_at', 'end_at', 'participants', ]
    filterset_fields = ['title', 'category', 'status', 'is_paid', 'is_survey_hidden', ]
    search_fields = ['title']

    def get_queryset(self):
        return Survey.objects.annotate(participants=Count('participant'))
