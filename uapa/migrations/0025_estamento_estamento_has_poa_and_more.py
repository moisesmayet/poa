# Generated by Django 4.0.3 on 2023-10-19 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uapa', '0024_remove_coordinacion_coordinacion_cargo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='estamento',
            name='estamento_has_poa',
            field=models.BooleanField(default=False, verbose_name='Tiene POA'),
        ),
        migrations.AddField(
            model_name='tipoestamento',
            name='tipo_faicon',
            field=models.CharField(default='', max_length=100, verbose_name='Fa Icon'),
        ),
        migrations.AlterField(
            model_name='estamento',
            name='estamento_name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
    ]
