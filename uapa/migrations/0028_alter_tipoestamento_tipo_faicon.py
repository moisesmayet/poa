# Generated by Django 4.0.3 on 2024-03-11 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uapa', '0027_remove_estamento_estamento_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoestamento',
            name='tipo_faicon',
            field=models.CharField(default='', max_length=100, verbose_name='Fa Icon'),
        ),
    ]
