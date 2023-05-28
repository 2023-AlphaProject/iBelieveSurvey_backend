from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from participant.models import Participant
from participant.permissions.writerPermission import ParticipantPermission
from participant.serializers.participantSerializer import ParticipantSerializer


class ParticipantDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ParticipantPermission]

    def get_object(self, pk):
        try:
            return Participant.objects.get(id=pk)
        except Participant.DoesNotExist:
            return Response({"error": "설문 답변이 존재하지 않거나 권한이 없기 때문에 설문 답변을 조회할 수 없습니다."})

    def get(self, request, survey_id, pk):
        participant = self.get_object(pk)
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data)

    def post(self, request, survey_id, pk):
        participant = self.get_object(pk)

        if not participant.survey.is_ongoing:
            return Response({"error": "설문이 진행 중이 아니기 때문에 설문에 참여할 수 없습니다."})

        serializer = ParticipantSerializer(participant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def put(self, request, survey_id, pk):
        participant = self.get_object(pk)

        if not participant.survey.is_ongoing:
            return Response({"error": "설문이 종료되었기 때문에 설문 답변을 수정할 수 없습니다."})

        serializer = ParticipantSerializer(participant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
