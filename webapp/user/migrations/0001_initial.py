# Generated by Django 4.1.6 on 2023-03-26 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 일시')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
                ('kakao_id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='카카오 id')),
                ('profile_image', models.CharField(max_length=255, null=True, verbose_name='프로필 사진')),
                ('real_name', models.CharField(max_length=30, verbose_name='실명')),
                ('phone_number', models.CharField(max_length=20, verbose_name='전화번호')),
                ('gender', models.IntegerField(verbose_name='성별')),
                ('birth', models.CharField(max_length=20, verbose_name='생년월일')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'user',
            },
        ),
    ]