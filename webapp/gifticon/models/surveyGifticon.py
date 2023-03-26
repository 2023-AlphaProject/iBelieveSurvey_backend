from django.db import models

from config.baseModel import BaseModel
from gifticon.models import Gifticon
from survey.models import Survey


class SurveyGifticon(BaseModel):
    class Meta:
        db_table = 'surveyGifticon'
        verbose_name = 'surveyGifticon'
        verbose_name_plural = 'surveyGifticons'

    survey = models.ForeignKey(
        Survey,
        verbose_name="설문 ID",
        on_delete=models.CASCADE,
        null=False,
    )

    gifticon = models.ForeignKey(
        Gifticon,
        verbose_name="설문 ID",
        on_delete=models.CASCADE,
        null=False,
    )

    count = models.BigIntegerField(
        verbose_name="기프티콘 총개수",
        null=False,
    )

    gifticonCount = models.BigIntegerField(
        verbose_name="기프티콘 개수",
        null=False,
    )

    receiver = models.CharField(
        verbose_name="받는 분",
        null=False,
        max_length=45,
    )
