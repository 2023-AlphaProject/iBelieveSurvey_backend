from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from cart.serializers import CartSerializer


class CartDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            # Retrieve a specific cart object for the user's survey with is_idle=True
            cart = Cart.objects.get(survey__user=self.request.user, survey__is_idle=True, pk=pk)
            return cart
        except Cart.DoesNotExist:
            return None

    def get(self, request, pk):
        cart = self.get_object(pk)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def update(self, request, pk):
        cart = self.get_object(pk)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart = self.get_object(pk)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
