# Generated by Django 4.0 on 2022-12-04 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistemadecompra', '0005_rename_imageurl_producto_imagenurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificacion',
            name='comentario',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='calificacion',
            name='puntaje',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]