# Generated by Django 4.0.3 on 2022-06-21 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poa', '0044_remove_evidencia_evidencia_actividad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidencia',
            name='evidencia_cronograma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poa.cronograma', verbose_name='Cronograma'),
        ),
    ]
