from django.db import models

from config.baseModel import BaseModel
from gifticon.models import Gifticon
from participant.models import Participant
from survey.models import Survey


class SurveyGifticon(BaseModel):
    class Meta:
        db_table = 'surveyGifticon'
        verbose_name = 'surveyGifticon'
        verbose_name_plural = 'surveyGifticons'

    survey = models.ForeignKey(
        Survey,
        verbose_name="설문",
        on_delete=models.CASCADE,
        null=False,
    )

    gifticon = models.ForeignKey(
        Gifticon,
        verbose_name="기프티콘",
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

    receiver = models.ForeignKey(
        Participant,
        verbose_name="받는 분",
        on_delete=models.CASCADE,
        null=False,
        max_length=45,
    )

    def save(self, *args, **kwargs):
        self.survey.is_idle = False
        self.survey.save()
        super().save(*args, **kwargs)
