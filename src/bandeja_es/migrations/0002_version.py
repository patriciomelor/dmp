# Generated by Django 3.1.1 on 2020-11-09 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel_carga', '0003_delete_version'),
        ('bandeja_es', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_version', models.CharField(max_length=5, verbose_name='Version documento')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Version')),
                ('comentario', models.FileField(blank=True, upload_to='proyecto/comentarios/')),
                ('archivo', models.FileField(blank=True, upload_to='proyecto/documentos/')),
                ('documento_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel_carga.documento')),
            ],
        ),
    ]