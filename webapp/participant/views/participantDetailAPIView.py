from rest_framework.response import Response
from rest_framework.views import APIView

from participant.models import Participant
from participant.serializers.participantSerializer import ParticipantSerializer


class ParticipantDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Participant.objects.get(id=pk)
        except Participant.DoesNotExist:
            return Response({"error": "설문이 존재하지 않기 때문에 설문 응답자를 가져올 수 없습니다."})

    def get(self, request, survey_id, pk):
        participant = self.get_object(pk)
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data)

    def put(self, request, survey_id, pk):
        participant = self.get_object(pk)

        if not participant.survey.is_ongoing:
            return Response({"error": "설문이 종료되었기 때문에 설문 응답을 수정할 수 없습니다."})

        serializer = ParticipantSerializer(participant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
