# Generated by Django 4.0.5 on 2022-12-08 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistemadecompra', '0012_remove_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='foto',
            field=models.ImageField(blank=True, upload_to='media/uploads/productos'),
        ),
    ]