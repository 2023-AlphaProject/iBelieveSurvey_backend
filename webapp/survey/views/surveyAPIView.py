from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import filters

from survey.models import Survey
from survey.serializers import SurveySerializer


class SurveyAPIView(CreateAPIView, ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['started_at', 'end_at', ]
    filterset_fields = ['title', 'category', 'is_idle', 'is_awarded', 'is_survey_hidden', ]
    search_fields = ['title']
    # TODO: filter, permission, pagination
