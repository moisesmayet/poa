# Generated by Django 4.0.3 on 2023-10-19 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_parametro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametro',
            name='parametro_name',
            field=models.CharField(max_length=40, unique=True, verbose_name='Nombre del Parámetro'),
        ),
    ]
