# Generated by Django 5.0.7 on 2024-07-21 23:33

import django.db.models.deletion
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
            field=models.ImageField(blank=True, db_column='ProImaPmg', null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='servicio',
            name='serimg',
            field=models.ImageField(blank=True, db_column='SerImaPng', null=True, upload_to='static/images/'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='clicon',
            field=models.CharField(db_column='CliCon', max_length=255),
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
            field=models.CharField(db_column='SerImaUrl', default='', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='tipopersonal',
            name='tippernom',
            field=models.CharField(db_column='TipPerNom', max_length=100),
        ),
        migrations.CreateModel(
            name='EventoProducto',
            fields=[
                ('evecod', models.AutoField(primary_key=True, serialize=False)),
                ('evedes', models.CharField(blank=True, max_length=150, null=True)),
                ('evefec', models.DateField()),
                ('cantidad', models.PositiveIntegerField()),
                ('notas', models.TextField(blank=True, null=True)),
                ('cliente', models.ForeignKey(db_column='CliDni', null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.cliente')),
                ('procod', models.ForeignKey(db_column='ProCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.producto')),
            ],
            options={
                'verbose_name': 'Evento de Producto',
                'verbose_name_plural': 'Eventos de Productos',
                'db_table': 'evento_producto',
            },
        ),
    ]
