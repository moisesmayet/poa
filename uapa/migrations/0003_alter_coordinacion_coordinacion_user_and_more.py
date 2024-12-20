# Generated by Django 4.0.3 on 2022-03-17 01:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uapa', '0002_coordinacion_coordinacion_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordinacion',
            name='coordinacion_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Coordinador(a)'),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='departamento_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='J. Departamento'),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='direccion_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Director(a)'),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='direccion_vice',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='uapa.vicerrectoria', verbose_name='Vicerrectoría'),
        ),
        migrations.AlterField(
            model_name='unidad',
            name='unidad_sede',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='uapa.sede', verbose_name='Sede'),
        ),
        migrations.AlterField(
            model_name='unidad',
            name='unidad_user',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='J. Unidad'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vicerrectoria',
            name='vice_sede',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='uapa.sede', verbose_name='Sede'),
        ),
        migrations.AlterField(
            model_name='vicerrectoria',
            name='vice_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Vicerrector(a)'),
        ),
    ]
