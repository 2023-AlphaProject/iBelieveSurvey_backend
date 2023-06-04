import uuid
from django.db import models
from config.baseModel import BaseModel

from survey.models import Survey
from template.models import Template


class Cart(BaseModel):
    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    uuid = models.UUIDField(
        verbose_name="장바구니 고유번호",
        primary_key=True,
        null=False,
        default=uuid.uuid4
    )

    survey = models.ForeignKey(
        Survey,
        verbose_name="설문",
        on_delete=models.CASCADE,
        null=False,
    )

    template = models.ForeignKey(
        Template,
        verbose_name="템플릿",
        on_delete=models.CASCADE,
        null=False,
    )

    quantity = models.PositiveIntegerField(
        verbose_name="상품 수량",
        null=False
    )

    @property
    def total_price(self):
        return self.template.product_price * self.quantity

    def __str__(self):
        return self.survey.title
