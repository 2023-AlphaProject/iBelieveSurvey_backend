from django.db import models

from config.baseModel import BaseModel


class Gifticon(BaseModel):

    class Meta:
        db_table = 'gifticon'
        verbose_name = 'Gifticon'
        verbose_name_plural = 'Gifticons'

    template = models.BigIntegerField(
        verbose_name="템플릿",
        null=False
    )

    price = models.BigIntegerField(
        verbose_name="가격",
        null=False
    )

    productImage = models.CharField(
        verbose_name="상품 이미지",
        null=False,
        max_length=45,
    )

    productName = models.CharField(
        verbose_name="상품 이름",
        null=False,
        max_length=45,
    )

    gifticonType = models.CharField(
        verbose_name="기프티콘 유형",
        null=False,
        max_length=45,
    )
