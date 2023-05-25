from django.db import models

from survey.models import Survey
from template.models import Template


class Cart(models.Model):
    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    survey = models.ForeignKey(Survey, verbose_name="설문", on_delete=models.CASCADE, null=False, related_name="survey_set")
    template = models.ForeignKey(Template, verbose_name="템플릿", on_delete=models.CASCADE, null=False, related_name="template_set")
    quantity = models.IntegerField(verbose_name="상품 수량", null=False)

    @property
    def total_price(self):
        return self.template.product_price * self.quantity
      
    def __str__(self):
        return self.survey.title
