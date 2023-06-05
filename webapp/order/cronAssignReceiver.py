from datetime import datetime

from order.models import Order
from participant.models import Participant


def assignReciver():
    orders = Order.objects.filter(receiver=None)

    if orders.count() == 0:
        print("이미 모든 설문에 당첨자가 지정되어 있습니다." + str(datetime.now()))
        return
    print("랜덤 당첨자 선정 시작 : " + str(datetime.now()))
    print("--------------------------------------------")
    exclude_receivers = []

    for order in orders:

        cart = order.cart
        survey = cart.survey

        if survey.is_end:
            available_receivers = Participant.objects.filter(survey=order.cart.survey).exclude(
                user__in=exclude_receivers)
            print(available_receivers)
            if available_receivers.exists():
                random_receiver = available_receivers.order_by('?').first()
                exclude_receivers.append(random_receiver.user)
                order.receiver = random_receiver
                order.save()
                print("설문 : " + order.cart.survey.title)
                print("당첨자 : " + random_receiver.user.realName)
                print("기프티콘 : " + order.cart.template.template_name)
                print("--------------------------------------------")

        else:
            print("설문 : " + order.cart.survey.title)
            print("해당 설문은 종료되지 않았기 때문에 당첨자를 지정하지 않고 다음 설문으로 넘어가 작업을 수행합니다.")

    print("랜덤 당첨자 선정 종료")
    print("--------------------------------------------")
    return
