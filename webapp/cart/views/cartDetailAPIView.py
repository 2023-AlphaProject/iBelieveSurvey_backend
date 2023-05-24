from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from cart.serializers import CartSerializer


class CartDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Cart.objects.get(id=pk)
        except Cart.DoesNotExist:
            raise NotFound("장바구니가 존재하지 않습니다.")

    def get(self, request, survey_id, cart_id):
        cart = self.get_object(cart_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, survey_id, cart_id):
        cart = self.get_object(cart_id)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, survey_id, cart_id):
        cart = self.get_object(cart_id)
        cart.delete()
        return Response(status=204)

# 1. 설문작성완료 = survey객체의 상태를 의미하는 일부 필드들은 다음과 같다. is_idle(T) / is_awarded(F) / is_ongoing(F) / is_done(F)
# 2. 설문작성완료했으니 기프티콘을 장바구니에 담자
# 3. 내가 담을 수 있는 템플릿의 목록들을 보여줘 : db에 저장된 template객체들 모두 가져오면 됨
# 카트 객체는 내가 만든 설문에 대해서만 list, post, retrieve, update, delete 될 수 있다.
# 4. cartListAPIView = post : is_idle=True 또는 is_ongoing=True일 때 내가 만든 설문조사에 해당하는 카트 객체에 특정 template을 n(=quantity)개 담을래
#                      get : is_idle=True 또는 is_ongoing=True일 때 내가 만든 설문조사에 해당하는 카트 객체들을 모두 보여줘
#
#    cartDetailAPIView = get : is_idle=True 또는 is_ongoing=True일 때 내가 만든 설문조사에 해당하는 특정 카트 객체를 상세보기할래
#                        update : is_idle=True 또는 is_ongoing=True일 때 내가 만든 설문조사에 해당하는 특정 카트 객체의 기프티콘을 수정하거나 수량을 수정할래
#                        delete : is_idle=True 또는 is_ongoing=True일 때 내가 만든 설문조사에 해당하는 특정 카트 객체를 삭제할래
# 4. 카트에 기프티콘들을 다 담았고 결제하러 가자
# 5. 결제완료 = is_idle(F) / is_awarded(F) / is_ongoing(T) / is_done(F)
# 6. 설문진행 (is_ongoing=True일 때 Cart객체 Retrieve 가능, Update 불가, Delete 불가)
