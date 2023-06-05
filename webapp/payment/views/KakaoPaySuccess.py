from django.shortcuts import redirect
from django.utils import timezone
from rest_framework.views import APIView

from cart.models import Cart
from order.models.order import Order
from survey.models import Survey


class KakaoPaySuccess(APIView):
    def get(self, request, survey_id):
        survey = Survey.objects.get(id=survey_id)
        survey.is_idle = False
        survey.is_paid = True
        survey.started_at = timezone.now()
        survey.save()

        existing_orders = Order.objects.filter(survey=survey).count()

        carts = Cart.objects.filter(survey=survey)

        # 이미 order객체가 생성된 것이 없다면 모든 cart객체들의 quantity만큼 order객체들을 생성한다.
        if existing_orders == 0:
            for cart in carts:
                for _ in range(cart.quantity):
                    Order.objects.create(survey=survey, template=cart.template, receiver=None)

        return redirect('http://localhost')
