# Generated by Django 4.0.3 on 2024-03-15 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poa', '0064_nota_nota_poa_nota_nota_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nota',
            name='nota_itemid',
            field=models.IntegerField(default=0, null=True, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='nota_itemname',
            field=models.CharField(max_length=100, null=True, verbose_name='Nombre'),
        ),
    ]
