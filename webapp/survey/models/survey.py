from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from config.baseModel import BaseModel
from config.exceptions.handler import validate_multiple
from user.models import User


class Survey(BaseModel):
    class Meta:
        db_table = 'survey'
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'

    title = models.CharField(verbose_name="설문 제목", max_length=255, null=False)
    thumbnail = models.URLField(verbose_name="설문 썸네일", max_length=255)
    category = models.ForeignKey('survey.Category', verbose_name="카테고리", on_delete=models.CASCADE, null=False,default=1)
    user = models.ForeignKey(User, verbose_name="사용자", on_delete=models.CASCADE, null=True)
    data = models.JSONField(verbose_name="설문 데이터", null=True)
    is_idle = models.BooleanField(verbose_name="설문 임시 저장 상태 여부", null=False, default=True)
    is_awarded = models.BooleanField(verbose_name="설문 보상 지급 완료 여부", null=False, default=False)
    is_survey_hidden = models.BooleanField(verbose_name="공개_비공개_여부", null=False, default=False)
    end_at = models.DateTimeField(verbose_name="설문 종료 일시", null=False)
    started_at = models.DateTimeField(verbose_name="설문 시작 일시", null=True)

    def __str__(self):
        return self.title

    def clean(self):
        validate_multiple(
            self.validate_end_at_field,
        )

    def validate_end_at_field(self):
        if self.started_at is not None and self.started_at > self.end_at:
            raise ValidationError('설문 종료 일시는 설문 생성 일시보다 빠를 수 없습니다.')

    def save(self, *args, **kwargs):
        if self.started_at is None and self.is_idle is False:
            self.started_at = timezone.now()
        self.clean()
        super().save(*args, **kwargs)

    @property
    def is_ongoing(self):
        if self.started_at is None:
            return False
        return timezone.now() <= self.end_at

    @property
    def is_done(self):
        if self.end_at < timezone.now() and not self.is_idle:
            return True
        return False

    # TODO: is_awarded 로직 추가
