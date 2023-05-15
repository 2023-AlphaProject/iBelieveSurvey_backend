from django.db import models

from survey.models import Survey
from user.models import User


class Participant(models.Model):
    class Meta:
        db_table = 'participant'
        verbose_name = 'participant'
        verbose_name_plural = 'participants'

    kakaoId = models.ForeignKey(User, verbose_name="설문 참여자", on_delete=models.CASCADE, null=False)
    survey = models.ForeignKey(Survey, verbose_name="설문", on_delete=models.CASCADE, null=False)
    json = models.JSONField(verbose_name="설문 데이터", null=False)
    created_at = models.DateTimeField(verbose_name="설문 참여 일시", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="설문 재참여 일시", auto_now=True)
