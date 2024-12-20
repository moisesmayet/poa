# Generated by Django 4.0.3 on 2024-03-18 23:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poa', '0069_nota_nota_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='bug_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='log',
            name='log_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='nota_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha'),
        ),
    ]
