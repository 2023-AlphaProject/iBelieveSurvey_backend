import os
from datetime import datetime, timezone

import boto3
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from survey.models import Survey
from user.models import User
from survey.permissions import IsSurveyOwnerOrReadOnly
from survey.serializers import SurveySerializer
from django.contrib.auth import authenticate, login


class WinningPercentageOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            if ordering[0] == 'winningPercentage' or ordering[0] == '-winningPercentage':
                is_descending = ordering[0].startswith('-')
                return sorted(queryset, key=lambda p: p.winningPercentage, reverse=is_descending)
            else:
                return queryset.order_by(*ordering)

class ParticipantsFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'under_ten' in request.query_params:
            return queryset.annotate(participant_count=Count('participant')).filter(participant_count__lt=10)
        if 'under_hundred' in request.query_params:
            return queryset.annotate(participant_count=Count('participant')).filter(participant_count__lt=100).filter(
                participant_count__gte=10)
        if 'over_hundred' in request.query_params:
            return queryset.annotate(participant_count=Count('participant')).filter(participant_count__gte=100)
        return queryset


class SurveyStatusFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        now = timezone.now()
        if 'ongoing' in request.query_params:
            return queryset.filter(started_at__lte=now, end_at__gte=now)
        if 'ended' in request.query_params:
            return queryset.filter(end_at__lt=now)
        return queryset


class SurveyAPIView(CreateAPIView, ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        ParticipantsFilter,
        SurveyStatusFilter,
        WinningPercentageOrderingFilter,
    ]
    ordering = ['id']
    ordering_fields = ['started_at', 'end_at', 'participants', 'winningPercentage']
    filterset_fields = ['title', 'category', 'is_paid', 'is_survey_hidden']
    search_fields = ['title']
    permission_classes = [IsSurveyOwnerOrReadOnly]

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
        serializer.save(writer=self.request.user)

    def create(self, request, *args, **kwargs):
        access = request.user
        if not access:
            return Response({'message': '로그인이 필요합니다. '}, status=400)
        else :
            # return Response({'message': '인증된 사용자입니다.'}, status=200)
            return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return Survey.objects.annotate(participants=Count('participant'))
