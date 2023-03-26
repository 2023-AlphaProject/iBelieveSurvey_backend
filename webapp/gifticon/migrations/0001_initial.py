# Generated by Django 4.1.6 on 2023-03-26 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gifticon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 일시')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
                ('if_sent', models.BigIntegerField(choices=[(0, 'not sent'), (1, 'sent')], default=0, verbose_name='기프티콘 전송 여부')),
                ('count', models.BigIntegerField(verbose_name='기프티콘 개수')),
                ('gifticon_type', models.CharField(max_length=20, verbose_name='기프티콘 종류')),
                ('sender', models.CharField(max_length=20, verbose_name='보내는 분')),
                ('receiver', models.CharField(max_length=20, verbose_name='받는 분')),
            ],
            options={
                'verbose_name': 'Gifticon',
                'verbose_name_plural': 'Gifticons',
                'db_table': 'gifticon',
            },
        ),
    ]
