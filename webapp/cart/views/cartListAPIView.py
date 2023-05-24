from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from cart.serializers import CartSerializer
from survey.models import Survey


class CartListAPIView(APIView):
    def get(self, request, survey_id):
        carts = Cart.objects.filter(survey_id=survey_id)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, survey_id):
        # survey_id를 가진 Survey 객체 가져오기
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return Response({'error':'해당 설문은 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 해당 Survey의 user 필드와 현재 요청의 사용자 비교
        if survey.user != request.user:
            return Response({'error':'해당 설문에 대한 장바구니 생성이 인가되지 않았습니다.'},
                            status=status.HTTP_403_FORBIDDEN)

        # 해당 Survey의 is_idle 필드 확인
        if not survey.is_idle:
            return Response({'error':'장바구니는 설문이 임시저장 상태일 때에만 가능합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # request에서 전달된 데이터 받기
        template_id = request.data.get('template_id')
        quantity = request.data.get('quantity')

        if not template_id:
            return Response({'error':'템플릿이 만료되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # Cart 생성
        cart = Cart.objects.create(
            survey=survey,
            template_id=template_id,
            quantity=quantity
        )

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
