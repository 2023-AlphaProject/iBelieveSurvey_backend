# Generated by Django 4.1.6 on 2023-04-17 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.BooleanField(verbose_name='성별'),
        ),
    ]