# Generated by Django 4.0.3 on 2022-04-25 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poa', '0036_alter_poadepartamento_unique_together_and_more'),
        ('uapa', '0023_alter_sede_options_alter_estamento_estamento_sub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coordinacion',
            name='coordinacion_cargo',
        ),
        migrations.RemoveField(
            model_name='coordinacion',
            name='coordinacion_sede',
        ),
        migrations.RemoveField(
            model_name='coordinacion',
            name='coordinacion_sub',
        ),
        migrations.RemoveField(
            model_name='coordinacion',
            name='coordinacion_user',
        ),
        migrations.RemoveField(
            model_name='coordinaciondepartamento',
            name='coordinacion',
        ),
        migrations.RemoveField(
            model_name='coordinaciondepartamento',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='coordinaciondireccion',
            name='coordinacion',
        ),
        migrations.RemoveField(
            model_name='coordinaciondireccion',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='coordinacionescuela',
            name='coordinacion',
        ),
        migrations.RemoveField(
            model_name='coordinacionescuela',
            name='escuela',
        ),
        migrations.RemoveField(
            model_name='departamento',
            name='departamento_cargo',
        ),
        migrations.RemoveField(
            model_name='departamento',
            name='departamento_sede',
        ),
        migrations.RemoveField(
            model_name='departamento',
            name='departamento_sub',
        ),
        migrations.RemoveField(
            model_name='departamento',
            name='departamento_user',
        ),
        migrations.RemoveField(
            model_name='departamentodireccion',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='departamentodireccion',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='departamentovicerrectoria',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='departamentovicerrectoria',
            name='vicerrectoria',
        ),
        migrations.RemoveField(
            model_name='direccion',
            name='direccion_cargo',
        ),
        migrations.RemoveField(
            model_name='direccion',
            name='direccion_user',
        ),
        migrations.RemoveField(
            model_name='direccion',
            name='direccion_vice',
        ),
        migrations.RemoveField(
            model_name='escuela',
            name='escuela_cargo',
        ),
        migrations.RemoveField(
            model_name='escuela',
            name='escuela_sede',
        ),
        migrations.RemoveField(
            model_name='escuela',
            name='escuela_sub',
        ),
        migrations.RemoveField(
            model_name='escuela',
            name='escuela_user',
        ),
        migrations.RemoveField(
            model_name='escueladireccion',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='escueladireccion',
            name='escuela',
        ),
        migrations.RemoveField(
            model_name='unidad',
            name='unidad_cargo',
        ),
        migrations.RemoveField(
            model_name='unidad',
            name='unidad_sede',
        ),
        migrations.RemoveField(
            model_name='unidad',
            name='unidad_sub',
        ),
        migrations.RemoveField(
            model_name='unidad',
            name='unidad_user',
        ),
        migrations.RemoveField(
            model_name='unidaddepartamento',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='unidaddepartamento',
            name='unidad',
        ),
        migrations.RemoveField(
            model_name='unidaddireccion',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='unidaddireccion',
            name='unidad',
        ),
        migrations.RemoveField(
            model_name='vicerrectoria',
            name='vice_cargo',
        ),
        migrations.RemoveField(
            model_name='vicerrectoria',
            name='vice_sede',
        ),
        migrations.RemoveField(
            model_name='vicerrectoria',
            name='vice_user',
        ),
        migrations.DeleteModel(
            name='Cargo',
        ),
        migrations.DeleteModel(
            name='Coordinacion',
        ),
        migrations.DeleteModel(
            name='CoordinacionDepartamento',
        ),
        migrations.DeleteModel(
            name='CoordinacionDireccion',
        ),
        migrations.DeleteModel(
            name='CoordinacionEscuela',
        ),
        migrations.DeleteModel(
            name='CoordinacionSub',
        ),
        migrations.DeleteModel(
            name='Departamento',
        ),
        migrations.DeleteModel(
            name='DepartamentoDireccion',
        ),
        migrations.DeleteModel(
            name='DepartamentoSub',
        ),
        migrations.DeleteModel(
            name='DepartamentoVicerrectoria',
        ),
        migrations.DeleteModel(
            name='Direccion',
        ),
        migrations.DeleteModel(
            name='Escuela',
        ),
        migrations.DeleteModel(
            name='EscuelaDireccion',
        ),
        migrations.DeleteModel(
            name='EscuelaSub',
        ),
        migrations.DeleteModel(
            name='Unidad',
        ),
        migrations.DeleteModel(
            name='UnidadDepartamento',
        ),
        migrations.DeleteModel(
            name='UnidadDireccion',
        ),
        migrations.DeleteModel(
            name='UnidadSub',
        ),
        migrations.DeleteModel(
            name='Vicerrectoria',
        ),
    ]
