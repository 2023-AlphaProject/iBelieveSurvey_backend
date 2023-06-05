from datetime import datetime

from cart.models import Cart
from order.models import Order
from participant.models import Participant


def assignReciver():
    orders = Order.objects.filter(receiver=None)
    if orders is None:
        print("이미 모든 설문에 당첨자가 지정되어 있습니다.")
        return
    print("랜덤 당첨자 선정 시작 : " + str(datetime.now()))
    for order in orders:
        cart_receivers = Order.objects.filter(cart=order.cart).values_list('receiver', flat=True)
        print(cart_receivers)
        available_receivers = Participant.objects.filter(survey=order.cart.survey).exclude(id__in=cart_receivers)
        print(available_receivers)
        if available_receivers.exists():
            random_receiver = available_receivers.order_by('?').first()
            order.receiver = random_receiver
            order.save()
            print("설문 : " + order.cart.survey.title)
            print("당첨자 : " + random_receiver.user.realName)
            print("기프티콘 : " + order.cart.template.template_name)
            print("--------------------------------------------")

    print("랜덤 당첨자 선정 종료")
    return

# 같은 cart에는 receiver가 중복되지 않도록 한다.
