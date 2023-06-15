from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone

from config.baseModel import BaseModel
from config.exceptions.handler import validate_multiple
from user.models import User


class Survey(BaseModel):
    class Meta:
        db_table = 'survey'
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'
        ordering = ['id']

    writer = models.ForeignKey(
        User,
        verbose_name="설문 작성자",
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )

    title = models.CharField(
        verbose_name="설문 제목",
        max_length=255,
        null=False,
    )

    outline = models.TextField(
        verbose_name="설문 개요",
        null=False,
    )

    thumbnail = models.ImageField(
        verbose_name="설문 썸네일",
        max_length=255,
        null=True,
    )

    category = models.ForeignKey(
        'survey.Category',
        verbose_name="카테고리",
        on_delete=models.CASCADE,
        null=False,
        default=1,
    )

    data = models.JSONField(
        verbose_name="설문 데이터",
        null=True,
    )

    is_idle = models.BooleanField(
        verbose_name="임시 저장 여부",
        null=False,
        default=True,
    )

    is_paid = models.BooleanField(
        verbose_name="결제 여부",
        null=False,
        default=False,
    )

    is_survey_hidden = models.BooleanField(
        verbose_name="공개_비공개_여부",
        null=False,
        default=False,
    )

    started_at = models.DateTimeField(
        verbose_name="설문 시작 일시",
        null=True,
    )

    end_at = models.DateField(
        verbose_name="설문 종료 일시",
        null=True,
    )

    @property
    def is_ongoing(self):
        if self.started_at is None or self.end_at is None:
            return False
        return self.started_at is not None and self.started_at <= timezone.now() and self.end_at >= timezone.now()

    @property
    def is_end(self):
        if self.end_at is None:
            return False
        return self.end_at < timezone.now()

    @property
    def winningPercentage(self):
        participants = self.participant_set.count()
        cart = apps.get_model('cart', 'Cart')
        gifticonsCount = cart.objects.filter(survey=self).aggregate(total_quantity=Sum('quantity'))[
            'total_quantity']
        if participants == 0:
            return 0
        try:
            percentage = round(gifticonsCount / participants * 100, 3)
        except TypeError:
            return 0
        if percentage > 100:
            return 100
        return percentage

    def __str__(self):
        return self.title

    def clean(self):
        validate_multiple(
            self.validate_end_at_field,
        )

    def validate_end_at_field(self):
        if self.started_at is not None and self.end_at is not None and self.started_at > self.end_at:
            raise ValidationError('설문 종료 일시는 설문 시작 일시보다 빠를 수 없습니다.')
        if self.end_at is not None and timezone.now() > self.end_at:
            raise ValidationError('설문 종료 일시는 현재 시간 보다 빠를 수 없습니다.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
