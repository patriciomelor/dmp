# Generated by Django 3.1.1 on 2022-01-11 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('status_encargado', '0010_auto_20211001_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='encargado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='responsable', to=settings.AUTH_USER_MODEL, verbose_name='Encargado'),
        ),
    ]
