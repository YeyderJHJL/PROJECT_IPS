# Generated by Django 5.0.7 on 2024-07-22 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_servicio_serima_alter_servicio_serdes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='proima',
            field=models.CharField(db_column='ProImaUrl', default='', max_length=400),
        ),
        migrations.AddField(
            model_name='producto',
            name='proimg',
            field=models.ImageField(blank=True, db_column='ProImaPmg', null=True, upload_to='static/images/'),
        ),
        migrations.AddField(
            model_name='servicio',
            name='serimg',
            field=models.ImageField(blank=True, db_column='SerImaPng', null=True, upload_to='static/images/'),
        ),
        migrations.AlterField(
            model_name='estadoregistro',
            name='estregnom',
            field=models.CharField(db_column='EstRegNom', max_length=100),
        ),
        migrations.AlterField(
            model_name='personal',
            name='percor',
            field=models.EmailField(blank=True, db_column='PerCor', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodes',
            field=models.CharField(blank=True, db_column='ProDes', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='pronom',
            field=models.CharField(db_column='ProNom', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='serima',
            field=models.CharField(db_column='SerImaUrl', default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='tipopersonal',
            name='tippernom',
            field=models.CharField(db_column='TipPerNom', max_length=100),
        ),
    ]
