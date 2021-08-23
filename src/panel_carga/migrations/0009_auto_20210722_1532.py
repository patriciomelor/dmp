# Generated by Django 3.1.1 on 2021-07-22 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel_carga', '0008_auto_20210722_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='umbral_desviacion_porcentual',
            field=models.FloatField(default=0, verbose_name='Umbral para Dviación Porcentual del Proyecto'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='umbral_documento_aprobado',
            field=models.IntegerField(default=0, verbose_name='Umbral para Documentos Aprobados'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='umbral_documento_atrasado',
            field=models.IntegerField(default=0, verbose_name='Umbral para Documentos Atrasados'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='umbral_revision_documento',
            field=models.IntegerField(default=0, verbose_name='Umbral para Revisiones Atrasadas'),
        ),
    ]
