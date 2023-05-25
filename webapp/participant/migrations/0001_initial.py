# Generated by Django 4.1.6 on 2023-05-25 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json', models.JSONField(verbose_name='설문 데이터')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='설문 참여 일시')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='설문 재참여 일시')),
            ],
            options={
                'verbose_name': 'participant',
                'verbose_name_plural': 'participants',
                'db_table': 'participant',
            },
        ),
    ]
