# Generated by Django 4.0.3 on 2022-04-04 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uapa', '0017_alter_cargo_cargo_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='cargo_name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Cargo'),
        ),
    ]
