# Generated by Django 3.1.1 on 2021-10-05 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandeja_es', '0009_auto_20210906_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paquete',
            name='asunto',
            field=models.CharField(max_length=300, verbose_name='Asunto'),
        ),
    ]
