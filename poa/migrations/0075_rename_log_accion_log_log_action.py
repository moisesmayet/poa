# Generated by Django 4.0.3 on 2024-04-08 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poa', '0074_bug_bug_poa_log_log_accion_log_log_poa_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='log_accion',
            new_name='log_action',
        ),
    ]
