from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.models import Cart
from cart.serializers import CartSerializer
from survey.models import Survey
from template.models import Template


class CartListAPIView(APIView):
    def get(self, request, survey_id):
        carts = Cart.objects.filter(survey_id=survey_id) # 해당 survey_id에 해당하는 cart 객체들을 가져옵니다.
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, survey_id):
        try:
            survey = Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            return Response({"error": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(survey=survey)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 1. 설문작성완료 = is_idle(T) / is_awarded(F) / is_ongoing(F) / is_done(F)
# 2. 기프티콘 담으러 가자 (is_idle=True일 때 Cart객체 Retrieve 가능, Update 가능, Delete 가능)
# 3. cartAPIView = get : is_idle=True일 때 내가 만든 설문조사에 해당하는 카트 객체들을 모두 보여줘
#                  post : is_idle=True일 때 내가 만든 설문조사에 해당하는 카트 객체에 특정 기프티콘을 n개 담을래
#    cartRetrieveUpdateDeleteAPIView = get : is_idle=True and is_ongoing=True 내가 만든 설문조사에 해당하는 특정 카트 객체를 상세보기할래
#                                      update : is_idle=True일 때 내가 만든 설문조사에 해당하는 특정 카트 객체의 기프티콘을 수정하거나 수량을 수정할래
#                                      delete : is_idle=True일 때 내가 만든 설문조사에 해당하는 특정 카트 객체를 삭제할래
# 4. 카트에 기프티콘들을 다 담았고 결제하러 가자
# 5. 결제완료 = is_idle(F) / is_awarded(F) / is_ongoing(T) / is_done(F)
# 6. 설문진행 (is_ongoing=True일 때 Cart객체 Retrieve 가능, Update 불가, Delete 불가)
#
