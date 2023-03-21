from config.baseModel import BaseModel
from django.db import models


class Survey(BaseModel):
    IDLE = 0
    ONGOING = 1
    DONE = 2
    AWARDED = 3

    class Meta:
        db_table = 'survey'
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'

    STATUS = (
        (IDLE, 'idle'),
        (ONGOING, 'ongoing'),
        (DONE, 'done'),
        (AWARDED, 'awarded'),
    )

    title = models.CharField(
        max_length=255,
        null=False,
    )

    thumbnail = models.URLField(
        max_length=255,
    )

    data = models.JSONField(
        null=False,
    )

    status = models.IntegerField(
        verbose_name="설문 상태",
        null=False,
        choices=STATUS,
        default=IDLE,
    )

    is_survey_hidden = models.BooleanField(
        verbose_name="공개_비공개_여부",
        null=False,
        default=False,
    )

    end_at = models.DateTimeField(
        verbose_name="설문 종료 일시",
        null=False,
    )
