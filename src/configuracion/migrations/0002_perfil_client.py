# Generated by Django 3.1.1 on 2021-02-04 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='client',
            field=models.BooleanField(default=True, verbose_name='Es cliente'),
        ),
    ]
