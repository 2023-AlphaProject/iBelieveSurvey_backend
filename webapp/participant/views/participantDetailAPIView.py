from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from survey.models import Survey

from participant.models import Participant
from participant.serializers.participantSerializer import ParticipantSerializer


class ParticipantDetailAPIView(RetrieveAPIView, UpdateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        try:
            return Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            return Response({"error": "설문 답변이 존재하지 않습니다."})

    def get(self, request, *args, **kwargs):
        """
        설문 작성자 또는 참여자가 해당 설문에 대한 특정 답변들을 조회합니다.
        """
        try:
            participant = self.get_object()
        except:
            return Response({"error": "답변이 존재하지 않습니다."})

        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        설문 참여자가 해당 설문에 대한 답변을 수정합니다.
        """
        try:
            participant = self.get_object()
        except:
            return Response({"error": "답변이 존재하지 않습니다."})

        if not self.get_survey().is_ongoing:
            return Response({"error": "설문이 진행 중이 아니므로 답변을 수정할 수 없습니다."})

        if request.user != participant.user:
            return Response({"error": "설문 참여자는 본인의 답변만 수정할 수 있습니다."})

        return self.update(request, *args, **kwargs)

    def get_survey(self):
        survey_id = self.kwargs['survey_id']
        survey = Survey.objects.get(id=survey_id)
        return survey
