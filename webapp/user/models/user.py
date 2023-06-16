from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """ModelManager definition for User Model"""

    def _create_user(self, email, password, **kwargs):
        user = self.model(
            email=email,
            **kwargs,
        )
        user.set_password(password)
        user.save()

    def create_user(self, email, password, **kwargs):
        """일반 유저 생성 메소드"""
        self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        """슈퍼 유저(superuser) 생성 메소드"""
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('realName', 'root')
        kwargs.setdefault('phoneNumber', '010-0000-0000')
        kwargs.setdefault('gender', 'male')
        kwargs.setdefault('birthyear', '1900')
        self._create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = (
        ('female', 'female'),
        ('male', 'male'),
    )

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    kakaoId = models.BigIntegerField(
        verbose_name="카카오 id",
        null=False,
        default=1,
    )

    email = models.CharField(
        verbose_name="카카오 이메일",
        max_length=255,
        null=False,
        unique=True,
    )

    realName = models.CharField(
        verbose_name="실명",
        max_length=30,
        null=True,
    )

    phoneNumber = models.CharField(
        verbose_name="전화번호",
        max_length=20,
        null=True,
    )

    gender = models.CharField(
        verbose_name="성별",
        choices=STATUS_CHOICES,
        max_length=10,
        default='male',
        null=True,
    )

    birthyear = models.CharField(
        verbose_name="출생연도",
        max_length=4,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self) -> str:
        return f'[{self.realName} ({self.email})'

    @property
    def hidden_realName(self):
        if self.realName is not None:
            if len(self.realName) == 2:
                return self.realName[0] + "*"
            else:
                return self.realName[0] + "*" * (len(self.realName) - 2) + self.realName[-1]
        else:
            return None

    @property
    def hidden_phoneNumber(self):
        if self.phoneNumber is not None:
            return self.phoneNumber[:3] + "-" + "*" * 4 + "-" + self.phoneNumber[-4:]
        else:
            return None
