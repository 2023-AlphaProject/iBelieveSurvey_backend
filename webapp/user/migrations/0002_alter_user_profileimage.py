# Generated by Django 4.1.6 on 2023-03-27 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profileImage',
            field=models.URLField(max_length=255, null=True, verbose_name='프로필 사진'),
        ),
    ]
