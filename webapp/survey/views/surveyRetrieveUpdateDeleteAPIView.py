from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    def get(self, request, *args, **kwargs):
        access = request.user
        if not access:
            return Response({'message': '로그인한 유저만 설문 조회 가능합니다. '}, status=400)
        else :
            # return Response({'message': '인증된 사용자입니다.'}, status=200)
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

    def delete(self, request, *args, **kwargs):
        """
        설문조사를 삭제합니다.
        진행중이거나 종료된 설문은 수정할 수 없습니다.
        """
        instance = self.get_object()
        if not instance.is_idle:
            return Response({'error': '설문이 진행중이거나 종료되어서 삭제할 수 없습니다.'}, status=400)
        return self.destroy(request, *args, **kwargs)
