# Generated by Django 4.1.6 on 2023-06-15 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        ('template', '0001_initial'),
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey', verbose_name='설문'),
        ),
        migrations.AddField(
            model_name='cart',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='template.template', verbose_name='템플릿'),
        ),
    ]
