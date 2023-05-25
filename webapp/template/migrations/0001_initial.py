# Generated by Django 4.1.6 on 2023-05-24 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_token', models.CharField(max_length=200, null=True, verbose_name='템플릿 토큰')),
                ('template_name', models.CharField(max_length=100, verbose_name='템플릿명')),
                ('template_trace_id', models.BigIntegerField(verbose_name='템플릿 ID')),
                ('order_template_status', models.CharField(max_length=100, verbose_name='템플릿 상태')),
                ('budget_type', models.CharField(max_length=100, verbose_name='한도 타입')),
                ('gift_sent_count', models.PositiveIntegerField(verbose_name='기발송 수')),
                ('bm_sender_name', models.CharField(max_length=100, verbose_name='발신자 명')),
                ('mc_image_url', models.URLField(verbose_name='메세지카드 이미지 url')),
                ('mc_text', models.TextField(verbose_name='메세지카드 입력값')),
                ('item_type', models.CharField(default='', max_length=50, verbose_name='상품 유형')),
                ('product_name', models.CharField(default='', max_length=20, verbose_name='상품명')),
                ('brand_name', models.CharField(default='', max_length=20, verbose_name='브랜드명')),
                ('product_image_url', models.URLField(default='', verbose_name='상품 이미지 url')),
                ('product_thumb_image_url', models.URLField(default='', verbose_name='상품 썸네일 이미지 url')),
                ('brand_image_url', models.URLField(default='', verbose_name='브랜드 이미지 url')),
                ('product_price', models.IntegerField(verbose_name='상품 가격')),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
                'db_table': 'template',
            },
        ),
    ]
