from django.db import models

from participant.models import Participant
from survey.models import Survey
from template.models.template import Template


# 아빌립서베이에 기프티콘 결제 요청오면 Cart의 quantity만큼 Order객체 생성
class Order(models.Model):
    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    survey = models.ForeignKey(Survey, verbose_name="설문", on_delete=models.CASCADE, null=False)
    template = models.ForeignKey(Template, verbose_name="템플릿", on_delete=models.CASCADE, null=False)
    receiver = models.ForeignKey(Participant, verbose_name="템플릿 수신자", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.receiver.user.realName
