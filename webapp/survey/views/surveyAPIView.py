from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from survey.models import Survey
from survey.permissions import IsSurveyOwnerOrReadOnly
from survey.serializers import SurveySerializer


class SurveyAPIView(CreateAPIView, ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering = ['id']
    ordering_fields = ['started_at', 'end_at', 'participants', ]
    filterset_fields = ['title', 'category', 'is_paid', 'is_survey_hidden', ]
    search_fields = ['title']
    permission_classes = [IsSurveyOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().create(request, *args, **kwargs)
        else:
            return Response({'error': '로그인이 필요합니다.'}, status=400)

    def get_queryset(self):
        return Survey.objects.annotate(participants=Count('participant'))
