from django.db import models

from config.baseModel import BaseModel


class User(BaseModel):

    gender = ((1, 'man'),
              (2, 'woman'))

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    kakaoId = models.CharField(
        verbose_name="카카오 id",
        max_length=255,
        null=False,
        primary_key=True,
    )

    profileImage = models.CharField(
        verbose_name="프로필 사진",
        max_length=255,
        null=True,
    )

    realName = models.CharField(
        verbose_name="실명",
        max_length=30,
        null=False,
    )

    phoneNumber = models.CharField(
        verbose_name="전화번호",
        max_length=20,
        null=False,
    )

    gender = models.BooleanField(
        verbose_name="성별",
        null=False,
        choices=gender
    )

    birth = models.DateField(
        verbose_name="생년월일",
        max_length=20,
        null=False,
    )
