from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from config.baseModel import BaseModel
from config.exceptions.handler import validate_multiple
from user.models import User


class Survey(BaseModel):
    STATUS_CHOICES = (
        ('NOT_STARTED', 'NOT_STARTED'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('END', 'END'),
    )

    class Meta:
        db_table = 'survey'
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'
        ordering = ['id']

    writer = models.ForeignKey(
        User,
        verbose_name="설문 작성자",
        on_delete=models.CASCADE,
        null=False,
    )

    title = models.CharField(
        verbose_name="설문 제목",
        max_length=255,
        null=False,
    )

    thumbnail = models.URLField(
        verbose_name="설문 썸네일",
        max_length=255,
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

    status = models.CharField(
        verbose_name="설문 상태",
        choices=STATUS_CHOICES,
        max_length=20,
        null=False,
        default='NOT_STARTED',
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

    end_at = models.DateTimeField(
        verbose_name="설문 종료 일시",
        null=False,
    )

    def __str__(self):
        return self.title

    def clean(self):
        validate_multiple(
            self.validate_end_at_field,
        )

    def validate_end_at_field(self):
        if self.started_at is not None and self.started_at > self.end_at:
            raise ValidationError('설문 종료 일시는 설문 시작 일시보다 빠를 수 없습니다.')
        if timezone.now() > self.end_at:
            raise ValidationError('설문 종료 일시는 현재 시간 보다 빠를 수 없습니다.')

    def save(self, *args, **kwargs):
        if self.started_at is None and self.is_paid:
            self.started_at = timezone.now()
        self.clean()
        super().save(*args, **kwargs)
