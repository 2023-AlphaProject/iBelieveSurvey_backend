# Generated by Django 4.1.6 on 2023-06-15 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_alter_survey_started_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='basic_thumbnail',
            field=models.CharField(max_length=255, null=True, verbose_name='설문 기본 썸네일'),
        ),
    ]