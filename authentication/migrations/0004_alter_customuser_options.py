# Generated by Django 4.0.3 on 2022-04-25 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_customuser_activation_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['first_name']},
        ),
    ]
