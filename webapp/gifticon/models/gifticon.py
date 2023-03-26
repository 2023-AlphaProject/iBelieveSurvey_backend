from django.db import models

from config.baseModel import BaseModel
from survey.models import Survey


class Gifticon(BaseModel):
    NOT_SENT = 0
    SENT = 1

    class Meta:
        db_table = 'gifticon'
        verbose_name = 'Gifticon'
        verbose_name_plural = 'Gifticons'

    SENT_STATUS = (
        (NOT_SENT, 'not sent'),
        (SENT, 'sent')
    )

    survey_id = models.ForeignKey(
        Survey,
        verbose_name="설문 ID",
        on_delete=models.CASCADE,
        null=False,
    )

    if_sent = models.BigIntegerField(
        verbose_name="기프티콘 전송 여부",
        null=False,
        choices=SENT_STATUS,
        default=0,
    )

    count = models.BigIntegerField(
        verbose_name="기프티콘 개수",
        null=False
    )

    gifticon_type = models.CharField(
        verbose_name="기프티콘 종류",
        null=False,
        max_length=20,
    )

    sender = models.CharField(
        verbose_name="보내는 분",
        null=False,
        max_length=20,
    )

    receiver = models.CharField(
        verbose_name="받는 분",
        null=False,
        max_length=20,
    )
