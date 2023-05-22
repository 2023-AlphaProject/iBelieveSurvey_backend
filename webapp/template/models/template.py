import hashlib

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Template(models.Model):
    class Meta:
        app_label = "template"
        db_table = "template"
        verbose_name = "Template"
        verbose_name_plural = "Templates"

    template_token = models.CharField(max_length=200, verbose_name="템플릿 토큰", null=True)  # 일단 null=True로 저장한 이후에 token 대입
    template_name = models.CharField(max_length=100, verbose_name="템플릿명", null=False)
    template_trace_id = models.BigIntegerField(verbose_name="템플릿 ID", null=False)
    order_template_status = models.CharField(max_length=100, verbose_name="템플릿 상태", null=False)  # REGISTERED, ALIVE, EXPIRED, CLOSED
    budget_type = models.CharField(max_length=100, verbose_name="한도 타입", null=False)  # UNLIMITED, LIMITED
    gift_sent_count = models.PositiveIntegerField(verbose_name="기발송 수", null=False)
    bm_sender_name = models.CharField(max_length=100, verbose_name="발신자 명", null=False)
    mc_image_url = models.URLField(max_length=200, verbose_name="메세지카드 이미지 url", null=False)
    mc_text = models.TextField(verbose_name="메세지카드 입력값", null=False)
    item_type = models.CharField(max_length=50, verbose_name="상품 유형", null=False, default="")
    product_name = models.CharField(max_length=20, verbose_name="상품명", null=False, default="")
    brand_name = models.CharField(max_length=20, verbose_name="브랜드명", null=False, default="")
    product_image_url = models.URLField(max_length=200, verbose_name="상품 이미지 url", null=False, default="")
    product_thumb_image_url = models.URLField(max_length=200, verbose_name="상품 썸네일 이미지 url", null=False, default="")
    brand_image_url = models.URLField(max_length=200, verbose_name="브랜드 이미지 url", null=False, default="")
    product_price = models.IntegerField(verbose_name="상품 가격", null=False)

    def __str__(self):
        return self.template_name

@receiver(pre_save, sender=Template)
def hash_template_token(sender, instance, **kwargs):
    value = instance.template_token
    if value is not None:
        hashed_value = hashlib.sha256(value.encode()).hexdigest()
        instance.template_token = hashed_value
