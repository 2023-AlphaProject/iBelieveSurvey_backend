from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from cart.serializers import CartSerializer


class CartDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return None

    def get(self, request, pk):
        # Retrieve a specific cart object
        cart = self.get_object(pk)
        if not cart:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Update a specific cart object
        cart = self.get_object(pk)
        if not cart:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Delete a specific cart object
        cart = self.get_object(pk)
        if not cart:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)

        cart.delete()
        return Response({'message': 'Cart deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

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
