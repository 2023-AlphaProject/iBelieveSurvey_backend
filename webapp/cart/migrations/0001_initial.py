# Generated by Django 4.1.6 on 2023-06-07 13:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 일시')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='장바구니 고유번호')),
                ('quantity', models.PositiveIntegerField(verbose_name='상품 수량')),
                ('is_sent', models.BooleanField(default=False, verbose_name='선물 발송 여부')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'db_table': 'cart',
            },
        ),
    ]
