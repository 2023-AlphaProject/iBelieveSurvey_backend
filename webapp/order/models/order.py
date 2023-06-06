from django.db import models

from cart.models.cart import Cart
from participant.models import Participant


# 아빌립서베이에 기프티콘 결제 요청오면 Cart의 quantity만큼 Order객체 생성
class Order(models.Model):
    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    cart = models.ForeignKey(Cart, verbose_name="장바구니", on_delete=models.CASCADE, null=False, default=None)
    receiver = models.ForeignKey(Participant, verbose_name="템플릿 수신자", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.receiver:
            return self.receiver.user.realName
        else:
            return "미정"

