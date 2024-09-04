# Generated by Django 4.0.3 on 2022-03-24 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uapa', '0010_vicerrectoria_vice_cargo'),
    ]

    operations = [
        migrations.AddField(
            model_name='direccion',
            name='direccion_cargo',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='uapa.cargo', verbose_name='Cargo'),
            preserve_default=False,
        ),
    ]
