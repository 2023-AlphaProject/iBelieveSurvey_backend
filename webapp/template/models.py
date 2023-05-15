import hashlib

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Template(models.Model):
    class Meta:
        db_table = "template"
        verbose_name = "Template"
        verbose_name_plural = "Templates"

    template_token = models.CharField(max_length=200, verbose_name="템플릿 토큰", null=False)  # 외부로 노출되지 않도록 주의
    template_name = models.CharField(max_length=100, verbose_name="템플릿명", null=False)
    template_trace_id = models.BigIntegerField(verbose_name="템플릿 ID", null=False)
    start_at = models.CharField(max_length=50, verbose_name="발송 가능 시작 일시", null=False)
    end_at = models.CharField(max_length=50, verbose_name="발송 가능 종료 일시", null=False)
    order_template_status = models.CharField(max_length=100, verbose_name="템플릿 상태", null=False)  # REGISTERED, ALIVE, EXPIRED, CLOSED
    budget_type = models.CharField(max_length=100, verbose_name="한도 타입", null=False)  # UNLIMITED, LIMITED
    gift_budget_count = models.IntegerField(verbose_name="발송 한도 수", null=False)
    gift_sent_count = models.IntegerField(verbose_name="기발송 수", null=False)
    gift_stock_count = models.IntegerField(verbose_name="발송 가능 수", null=False)
    bm_sender_name = models.CharField(max_length=100, verbose_name="발신자 명", null=False)
    mc_image_url = models.URLField(max_length=200, verbose_name="메세지카드 입력값", null=False)
    mc_text = models.TextField(verbose_name="메세지카드 입력값", null=False)
    product = models.JSONField(verbose_name="템플릿 상품 정보", null=False)


@receiver(pre_save, sender=Template)
def hash_template_token(sender, instance, **kwargs):
    value = instance.template_token
    hashed_value = hashlib.sha256(value.encode()).hexdigest()
    instance.template_token = hashed_value
