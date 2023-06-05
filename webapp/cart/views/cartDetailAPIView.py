from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import CartDetailSerializer
from survey.models import Survey


class CartDetailAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'uuid'
    query_set = Cart.objects.all()
    serializer_class = CartDetailSerializer

    def get_object(self):
        uuid = self.kwargs['uuid']
        try:
            return Cart.objects.get(uuid=uuid)
        except Cart.DoesNotExist:
            return Response({"error": "장바구니가 존재하지 않습니다."})

    def get(self, request, *args, **kwargs):
        """
        설문 작성자가 장바구니에 담았던 특정 템플릿 묶음을 반환합니다.
        """
        self.check_cart_exist()

        if not self.request.user.is_authenticated:
            return Response({"error": "장바구니를 조회하기 위해선 로그인이 필요합니다."})

        if request.user != self.get_survey().writer:
            return Response({"error": "설문 작성자 본인만이 해당 설문의 장바구니를 조회할 수 있습니다."})

        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        설문 작성자가 장바구니에 담았던 특정 템플릿 묶음을 수정합니다.
        """
        self.check_cart_exist()

        # 애초에 get 예외처리에 걸리지만, 일단 예외처리함
        if not self.request.user.is_authenticated:
            return Response({"error": "장바구니를 수정하기 위해선 로그인이 필요합니다."})

        if request.user != self.get_survey().writer:
            return Response({"error": "설문 작성자 본인만이 해당 설문의 장바구니를 수정할 수 있습니다."})

        if not self.get_survey().is_idle:
            return Response({"error": "설문이 시작된 후에는 장바구니를 수정할 수 없습니다."})

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        설문 작성자가 장바구니에 담았던 특정 템플릿 묶음을 삭제합니다.
        """
        self.check_cart_exist()

        # 애초에 get 예외처리에 걸리지만, 일단 예외처리함
        if not self.request.user.is_authenticated:
            return Response({"error": "장바구니를 삭제하기 위해선 로그인이 필요합니다."})

        if request.user != self.get_survey().writer:
            return Response({"error": "설문 작성자 본인만이 해당 설문의 장바구니를 삭제할 수 있습니다."})

        return self.destroy(request, *args, **kwargs)

    def get_survey(self):
        survey_id = self.kwargs['survey_id']
        survey = Survey.objects.get(id=survey_id)
        return survey

    def check_cart_exist(self):
        try:
            cart = self.get_object()
        except:
            return Response({"error": "장바구니가 존재하지 않습니다."})
