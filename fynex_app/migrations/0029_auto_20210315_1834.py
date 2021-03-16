# Generated by Django 3.1.4 on 2021-03-15 23:34

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fynex_app', '0028_auto_20210315_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examen',
            name='documento_ruta',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=200)),
        ),
        migrations.AlterField(
            model_name='medico',
            name='documento_identificacion',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=30)),
        ),
        migrations.AlterField(
            model_name='medico',
            name='telefono',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=30)),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='mensaje',
            field=django_cryptography.fields.encrypt(models.TextField()),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='telefono',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=30)),
        ),
        migrations.AlterField(
            model_name='preexistenciamedica',
            name='descripcion',
            field=django_cryptography.fields.encrypt(models.TextField()),
        ),
    ]
