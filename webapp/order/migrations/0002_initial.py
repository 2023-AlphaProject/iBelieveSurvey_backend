# Generated by Django 4.1.6 on 2023-05-25 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('participant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='participant.participant', verbose_name='템플릿 수신자'),
        ),
    ]
