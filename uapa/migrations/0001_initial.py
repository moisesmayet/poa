# Generated by Django 4.0.3 on 2022-03-16 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinacion_name', models.CharField(max_length=100, verbose_name='Coordinación')),
            ],
            options={
                'verbose_name': 'Coordinación',
                'verbose_name_plural': 'Coordinaciones',
                'db_table': 'Coordinacion',
                'ordering': ['coordinacion_name'],
            },
        ),
        migrations.CreateModel(
            name='CoordinacionSub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinacionsub_name', models.CharField(max_length=100, verbose_name='Coordinación Subordinación')),
            ],
            options={
                'verbose_name': 'CoordinaciónSub',
                'verbose_name_plural': 'CoordinaciónSubs',
                'db_table': 'CoordinacionSub',
                'ordering': ['coordinacionsub_name'],
            },
        ),
        migrations.CreateModel(
            name='DeparatamentoSub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamentosub_name', models.CharField(max_length=100, verbose_name='Deparatamento Subordinación')),
            ],
            options={
                'verbose_name': 'DeparatamentoSub',
                'verbose_name_plural': 'DeparatamentoSubs',
                'db_table': 'DeparatamentoSub',
                'ordering': ['departamentosub_name'],
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento_name', models.CharField(max_length=100, verbose_name='Departamento')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'db_table': 'Departamento',
                'ordering': ['departamento_name'],
            },
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion_name', models.CharField(max_length=100, verbose_name='Dirección')),
            ],
            options={
                'verbose_name': 'Dirección',
                'verbose_name_plural': 'Direcciones',
                'db_table': 'Direccion',
                'ordering': ['direccion_name'],
            },
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sede_name', models.CharField(max_length=100, verbose_name='Sede')),
            ],
            options={
                'verbose_name': 'Sede',
                'verbose_name_plural': 'Sedes',
                'db_table': 'Sede',
                'ordering': ['sede_name'],
            },
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidad_name', models.CharField(max_length=100, verbose_name='Unidad')),
                ('unidad_sede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.sede', verbose_name='Sede')),
            ],
            options={
                'verbose_name': 'Unidad',
                'verbose_name_plural': 'Unidades',
                'db_table': 'Unidad',
                'ordering': ['unidad_name'],
            },
        ),
        migrations.CreateModel(
            name='UnidadSub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidadsub_name', models.CharField(max_length=100, verbose_name='Unidad Subordinación')),
            ],
            options={
                'verbose_name': 'UnidadSub',
                'verbose_name_plural': 'UnidadSubs',
                'db_table': 'UnidadSub',
                'ordering': ['unidadsub_name'],
            },
        ),
        migrations.CreateModel(
            name='Vicerrectoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vice_name', models.CharField(max_length=100, verbose_name='Vicerrectoría')),
                ('vice_sede', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='uapa.sede', verbose_name='Sede')),
            ],
            options={
                'verbose_name': 'Vicerrectoría',
                'verbose_name_plural': 'Vicerrectorías',
                'db_table': 'Vicerrectoria',
                'ordering': ['vice_name'],
            },
        ),
        migrations.CreateModel(
            name='UnidadDireccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.direccion', verbose_name='Dirección')),
                ('unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.unidad', verbose_name='Unidad')),
            ],
            options={
                'verbose_name': 'UnidadDireccion',
                'verbose_name_plural': 'UnidadDireccions',
                'db_table': 'UnidadDireccion',
                'ordering': ['unidad'],
            },
        ),
        migrations.CreateModel(
            name='UnidadDepartamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.departamento', verbose_name='Departamento')),
                ('unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.unidad', verbose_name='Unidad')),
            ],
            options={
                'verbose_name': 'UnidadDepartamento',
                'verbose_name_plural': 'UnidadDepartamentos',
                'db_table': 'UnidadDepartamento',
                'ordering': ['unidad'],
            },
        ),
        migrations.AddField(
            model_name='unidad',
            name='unidad_sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.unidadsub', verbose_name='Subordinación'),
        ),
        migrations.AddField(
            model_name='direccion',
            name='direccion_vice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='uapa.vicerrectoria', verbose_name='Vicerrectoría'),
        ),
        migrations.CreateModel(
            name='DepartamentoVicerrectoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.departamento', verbose_name='Departamento')),
                ('vicerrectoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.vicerrectoria', verbose_name='Vicerrectoria')),
            ],
            options={
                'verbose_name': 'DepartamentoVicerrectoria',
                'verbose_name_plural': 'DepartamentoVicerrectorias',
                'db_table': 'DepartamentoVicerrectoria',
                'ordering': ['departamento'],
            },
        ),
        migrations.CreateModel(
            name='DepartamentoDireccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.departamento', verbose_name='Departamento')),
                ('direccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.direccion', verbose_name='Dirección')),
            ],
            options={
                'verbose_name': 'DepartamentoDireccion',
                'verbose_name_plural': 'DepartamentoDireccions',
                'db_table': 'DepartamentoDireccion',
                'ordering': ['departamento'],
            },
        ),
        migrations.AddField(
            model_name='departamento',
            name='departamento_sede',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.sede', verbose_name='Sede'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='departamento_sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.deparatamentosub', verbose_name='Subordinación'),
        ),
        migrations.CreateModel(
            name='CoordinacionDireccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.coordinacion', verbose_name='Coordinación')),
                ('direccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.direccion', verbose_name='Dirección')),
            ],
            options={
                'verbose_name': 'CoordinacionDireccion',
                'verbose_name_plural': 'CoordinacionDireccions',
                'db_table': 'CoordinacionDireccion',
                'ordering': ['coordinacion'],
            },
        ),
        migrations.CreateModel(
            name='CoordinacionDepartamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.coordinacion', verbose_name='Coordinación')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.departamento', verbose_name='Departamento')),
            ],
            options={
                'verbose_name': 'CoordinacionDepartamento',
                'verbose_name_plural': 'CoordinacionDepartamentos',
                'db_table': 'CoordinacionDepartamento',
                'ordering': ['coordinacion'],
            },
        ),
        migrations.AddField(
            model_name='coordinacion',
            name='coordinacion_sede',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.sede', verbose_name='Sede'),
        ),
        migrations.AddField(
            model_name='coordinacion',
            name='coordinacion_sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uapa.coordinacionsub', verbose_name='Subordinación'),
        ),
    ]
