# Generated by Django 4.0.3 on 2022-06-21 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poa', '0043_remove_actividad_actividad_cumplimiento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evidencia',
            name='evidencia_actividad',
        ),
        migrations.AddField(
            model_name='evidencia',
            name='evidencia_cronograma',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='poa.cronograma', verbose_name='Cronograma'),
        ),
    ]
