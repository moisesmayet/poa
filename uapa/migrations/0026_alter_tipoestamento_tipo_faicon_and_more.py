# Generated by Django 4.0.3 on 2023-10-19 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uapa', '0025_estamento_estamento_has_poa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoestamento',
            name='tipo_faicon',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Fa Icon'),
        ),
        migrations.AlterUniqueTogether(
            name='estamento',
            unique_together={('estamento_name', 'estamento_sede')},
        ),
    ]
