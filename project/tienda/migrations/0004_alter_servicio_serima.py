# Generated by Django 5.0.7 on 2024-07-15 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0003_producto_proima_producto_proimg_servicio_serimg_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='serima',
            field=models.CharField(db_column='SerImaUrl', default='', max_length=400, null=True),
        ),
    ]