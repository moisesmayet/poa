# Generated by Django 4.0.3 on 2024-04-07 19:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0006_typenotification_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notification',
            new_name='Notificacion',
        ),
        migrations.RenameModel(
            old_name='TypeNotification',
            new_name='TipoNotificacion',
        ),
        migrations.AlterModelOptions(
            name='tiponotificacion',
            options={'ordering': ['id'], 'verbose_name': 'TipoNotificacion', 'verbose_name_plural': 'TipoNotificaciones'},
        ),
        migrations.RenameField(
            model_name='tiponotificacion',
            old_name='type_code',
            new_name='tipo_code',
        ),
        migrations.RenameField(
            model_name='tiponotificacion',
            old_name='type_name',
            new_name='tipo_name',
        ),
        migrations.AlterModelTable(
            name='notificacion',
            table='Notificacion',
        ),
        migrations.AlterModelTable(
            name='tiponotificacion',
            table='TipoNotificacion',
        ),
    ]
