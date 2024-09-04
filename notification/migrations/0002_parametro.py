# Generated by Django 4.0.3 on 2023-10-19 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parametro_name', models.CharField(max_length=10, unique=True, verbose_name='Nombre del Parámetro')),
                ('parametro_value', models.CharField(max_length=100, verbose_name='Valor del Parámetro')),
            ],
            options={
                'verbose_name': 'Parámetros',
                'verbose_name_plural': 'Parámetros',
                'db_table': 'Parametro',
                'ordering': ['parametro_name'],
            },
        ),
    ]
