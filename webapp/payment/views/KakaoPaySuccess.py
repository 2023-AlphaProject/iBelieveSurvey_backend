from datetime import date

from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView

from cart.models.cart import Cart
from order.models.order import Order
from survey.models.survey import Survey


class KakaoPaySuccess(APIView):
    def get(self, request, survey_id):
        """
        카카오페이 결제 성공 시, 해당 설문의 상태를 변경합니다.
        """
        survey = Survey.objects.get(id=survey_id)
        survey.is_idle = False
        survey.is_paid = True
        survey.started_at = date.today()
        survey.save()

        carts = Cart.objects.filter(survey=survey)
        for cart in carts:
            existing_orders = Order.objects.filter(cart=cart).count()
            if existing_orders == 0:
                for _ in range(cart.quantity):
                    Order.objects.create(cart=cart, receiver=None)

        return redirect(settings.FRONTEND_URL + "survey/" + str(survey_id))
