from django.db import models

from config.baseModel import BaseModel


class User(BaseModel):
    MAN = 1
    WOMAN = 2

    gender = ((MAN, 'man'),
              (WOMAN, 'woman'))

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    kakao_id = models.CharField(
        verbose_name="카카오 id",
        max_length=255,
        null=False,
        primary_key=True,
    )

    profile_image = models.CharField(
        verbose_name="프로필 사진",
        max_length=255,
        null=True,
    )

    real_name = models.CharField(
        verbose_name="실명",
        max_length=30,
        null=False,
    )

    phone_number = models.CharField(
        verbose_name="전화번호",
        max_length=20,
        null=False,
    )

    gender = models.IntegerField(
        verbose_name="성별",
        null=False,
        choices=gender
    )

    birth = models.DateTimeField(
        verbose_name="생년월일",
        max_length=20,
        null=False,
    )
