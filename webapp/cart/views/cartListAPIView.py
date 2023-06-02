from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import CartListSerializer
from survey.models import Survey
from template.models import Template


class CartListAPIView(ListCreateAPIView):
    serializer_class = CartListSerializer
    ordering = ['template']
    queryset = Cart.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "장바구니를 조회하기 위해선 로그인이 필요합니다."})

        survey = self.get_survey()
        if self.request.user != survey.writer:
            return Response({"error": "설문 작성자 본인만이 해당 설문의 장바구니를 조회할 수 있습니다."})

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "장바구니에 기프티콘을 담기 위해선 로그인이 필요합니다."})

        # 애초에 get 예외처리에 걸리지만, 일단 예외처리함
        if self.request.user != self.get_survey().writer:
            return Response({"error": "설문 작성자 본인만이 해당 설문의 장바구니에 기프티콘을 담을 수 있습니다."})

        if not self.get_survey().is_idle:
            return Response({"error": "설문이 시작된 후에는 장바구니에 기프티콘을 담을 수 없습니다."})

        template_id = request.data.get("template")
        if template_id is None:
            return Response({"error": "장바구니에 기프티콘을 담아야 합니다."})

        try:
            template = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return Response({"error": "유효하지 않은 템플릿입니다."})

        return self.create(request, *args, **kwargs)

    def get_survey(self):
        survey_id = self.kwargs['survey_id']
        survey = Survey.objects.get(id=survey_id)
        return survey
