from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser

from survey.models import Survey
from survey.serializers import SurveySerializer


class WinningPercentageOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            if ordering[0] == 'winningPercentage' or ordering[0] == '-winningPercentage':
                is_descending = ordering[0].startswith('-')
                return sorted(queryset, key=lambda p: p.winningPercentage, reverse=is_descending)
            else:
                return queryset.order_by(*ordering)


class SurveyAPIView(CreateAPIView, ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        WinningPercentageOrderingFilter,
    ]
    ordering = ['id']
    ordering_fields = ['started_at', 'end_at', 'participants', 'winningPercentage']
    filterset_fields = ['title', 'category', 'is_paid', 'is_survey_hidden', ]
    search_fields = ['title']
    parser_classes = (FormParser, MultiPartParser)

    # permission_classes = [IsSurveyOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        """
        설문조사 목록을 조회합니다.
        """
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        설문조사를 생성합니다.
        """
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            serializer.save(writer=self.request.user)
        except:
            serializer.save(writer=None)

    # def create(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return super().create(request, *args, **kwargs)
    #     else:
    #         return Response({'error': '로그인이 필요합니다.'}, status=400)

    def get_queryset(self):
        return Survey.objects.annotate(participants=Count('participant'))
