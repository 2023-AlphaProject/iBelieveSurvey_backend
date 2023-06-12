import os
from datetime import datetime

import boto3
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from config.settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

from survey.models import Survey
from survey.permissions import IsSurveyOwnerOrReadOnly
from survey.serializers import *


class SurveyRetrieveUpdateDestoryAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSurveyOwnerOrReadOnly, IsAuthenticated]
    queryset = Survey.objects.all()
    lookup_url_kwarg = 'survey_id'

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return SurveySerializer

        instance = self.get_object()

        HIDDEN_END_SURVEY = instance.is_survey_hidden and instance.is_end
        NOT_HIDDEN_END_SURVEY = not instance.is_survey_hidden and instance.is_end
        NOT_STARTED_SURVEY = instance.is_idle

        if NOT_STARTED_SURVEY:
            return SurveyRetrieveSerializer
        elif HIDDEN_END_SURVEY:
            return HiddenEndSurveySerializer
        elif NOT_HIDDEN_END_SURVEY:
            return NotHiddenEndSurveySerializer
        else:
            return SurveySerializer

    def perform_update(self, serializer):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key_id=AWS_SECRET_ACCESS_KEY
        )

        image = self.request.FILES.get('filename')
        if image:
            # 기존 thumbnail 삭제
            instance = self.get_object()
            if instance.thumbnail:
                file_name = os.path.basename(instance.thumbnail)
                s3_client.delete_object(
                    Bucket=AWS_STORAGE_BUCKET_NAME,  # S3 버킷 이름
                    Key=file_name,  # 삭제할 파일의 경로와 이름
                )

            # 새로운 thumbnail 업로드
            image_time = (str(datetime.now())).replace(" ", "")
            image_type = (image.content_type).split("/")[1]
            s3_client.upload_fileobj(
                image,  # 업로드할 파일 객체
                "ibelievesurvey-be-deploy",  # S3 버킷 이름
                image_time + "." + image_type,  # S3 버킷에 저장될 파일의 경로와 이름
                ExtraArgs={"ContentType": image.content_type}  # 파일의 ContentType 설정
            )
            image_url = os.environ.get("S3_URL") + image_time + "." + image_type
            image_url = image_url.replace(" ", "/")

            serializer.save(writer=self.request.user, thumbnail=image_url)
        else:
            serializer.save(writer=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        설문조사를 조회합니다.
        로그인한 유저만 조회 가능합니다.
        """
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        설문조사를 수정합니다.
        진행중이거나 종료된 설문은 수정할 수 없습니다.
        """
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        설문조사를 수정합니다.
        진행중이거나 종료된 설문은 수정할 수 없습니다.
        """
        return super().patch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not instance.is_idle:
            return Response({'error': '설문이 진행중이거나 종료되어서 수정할 수 없습니다.'}, status=400)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_destroy(self, instance):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key_id=AWS_SECRET_ACCESS_KEY
        )

        # thumbnail 삭제
        if instance.thumbnail:
            file_name = os.path.basename(instance.thumbnail)
            s3_client.delete_object(
                Bucket=AWS_STORAGE_BUCKET_NAME,  # S3 버킷 이름
                Key=file_name,  # 삭제할 파일의 경로와 이름
            )

        instance.delete()

    def delete(self, request, *args, **kwargs):
        """
        설문조사를 삭제합니다.
        진행중이거나 종료된 설문은 수정할 수 없습니다.
        """
        instance = self.get_object()
        if not instance.is_idle:
            return Response({'error': '설문이 진행중이거나 종료되어서 삭제할 수 없습니다.'}, status=400)
        return self.destroy(request, *args, **kwargs)
