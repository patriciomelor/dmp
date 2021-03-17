# Generated by Django 3.1.1 on 2021-03-08 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel_carga', '0002_auto_20210308_1241'),
        ('bandeja_es', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='proyecto',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='proyecto', to='panel_carga.proyecto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='prevversion',
            name='prev_revision',
            field=models.IntegerField(choices=[('', '------'), (1, 'B'), (2, 'C'), (3, 'D'), (4, 'E'), (5, '0'), (6, '1'), (7, '2'), (8, '3'), (9, '4'), (10, '5')], verbose_name='Revisión'),
        ),
        migrations.AlterField(
            model_name='version',
            name='revision',
            field=models.IntegerField(choices=[('', '------'), (1, 'B'), (2, 'C'), (3, 'D'), (4, 'E'), (5, '0'), (6, '1'), (7, '2'), (8, '3'), (9, '4'), (10, '5')], verbose_name='Revisión'),
        ),
    ]