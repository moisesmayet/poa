# Generated by Django 4.0.3 on 2024-03-17 04:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poa', '0066_remove_poa_poa_notas'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nota',
            options={'ordering': ['nota_date'], 'verbose_name': 'Nota', 'verbose_name_plural': 'Notas'},
        ),
        migrations.AddField(
            model_name='nota',
            name='nota_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Fecha'),
        ),
    ]
