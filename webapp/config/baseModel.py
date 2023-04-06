from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="생성 일시",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="수정 일시",
        auto_now=True,
    )

    is_deleted = models.BooleanField(
        verbose_name="삭제 여부",
        default=False,
    )

    class Meta:
        abstract = True
