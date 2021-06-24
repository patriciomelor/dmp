# Generated by Django 3.1.1 on 2021-06-24 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status_encargado', '0003_auto_20210622_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='media/respuestas/', verbose_name='Archivo'),
        ),
        migrations.AddField(
            model_name='tarea',
            name='comentarios',
            field=models.TextField(default='', verbose_name='Comentarios'),
            preserve_default=False,
        ),
    ]
