# Generated by Django 3.1.4 on 2021-03-15 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fynex_app', '0026_auto_20210314_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plannutricional',
            name='dif_carbohidratos',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='plannutricional',
            name='dif_grasas',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='plannutricional',
            name='dif_proteinas',
            field=models.TextField(),
        ),
    ]
