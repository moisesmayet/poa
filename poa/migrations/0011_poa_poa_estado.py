# Generated by Django 4.0.3 on 2022-03-25 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poa', '0010_alter_poaestado_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='poa',
            name='poa_estado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='poa.poaestado', verbose_name='Estado'),
            preserve_default=False,
        ),
    ]
