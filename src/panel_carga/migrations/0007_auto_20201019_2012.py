# Generated by Django 3.1.1 on 2020-10-19 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel_carga', '0006_auto_20201019_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='num_documento',
            field=models.CharField(max_length=100, unique=True, verbose_name='Codigo Documento'),
        ),
    ]
