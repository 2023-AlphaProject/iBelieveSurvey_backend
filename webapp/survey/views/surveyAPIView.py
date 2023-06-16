import os
from datetime import datetime

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
import jwt
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
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key_id=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

        image = self.request.FILES['filename']
        image_time = (str(datetime.now())).replace(" ", "")
        image_type = (image.content_type).split("/")[1]
        aws_storage_bucket_name = os.environ.get("AWS_STORAGE_BUCKET_NAME")
        s3_client.upload_fileobj(
            image,  # 업로드할 파일 객체
            aws_storage_bucket_name,  # S3 버킷 이름
            image_time + "." + image_type,  # S3 버킷에 저장될 파일의 경로와 이름
            ExtraArgs={"ContentType": image.content_type}  # 파일의 ContentType 설정
        )
        image_url = os.environ.get("S3_URL") + image_time + "." + image_type
        image_url = image_url.replace(" ", "/")

        serializer.save(writer=self.request.user, thumbnail=image_url)

    def create(self, request, *args, **kwargs):
        access = request.user
        if not access:
            return Response({'message': '토큰 없음'}, status=200)
        else :
            return Response({'message': '토큰 있음!!!!'}, status=200)

    def get_queryset(self):
        return Survey.objects.annotate(participants=Count('participant'))
