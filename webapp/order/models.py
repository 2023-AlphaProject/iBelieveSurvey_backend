import hashlib

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    template_token = models.CharField(max_length=200, verbose_name="템플릿 토큰", null=True)  # 외부로 노출되지 않도록 주의
    receiver = models.ForeignKey(Participant, verbose_name="설문 객체", on_delete=models.CASCADE, null=False)


@receiver(pre_save, sender=Template)
def hash_template_token(sender, instance, **kwargs):
    value = instance.template_token
    if value is not None:
        hashed_value = hashlib.sha256(value.encode()).hexdigest()
        instance.template_token = hashed_value
