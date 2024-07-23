# Generated by Django 5.0.7 on 2024-07-23 15:48

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoariaProducto',
            fields=[
                ('catprocod', models.AutoField(db_column='CatProCod', primary_key=True, serialize=False)),
                ('catpronom', models.CharField(db_column='CatProNom', max_length=60, unique=True)),
            ],
            options={
                'verbose_name': 'Categoría de Producto',
                'verbose_name_plural': 'Categorías de Productos',
                'db_table': 'categoaria_producto',
            },
        ),
        migrations.CreateModel(
            name='CategoariaServicio',
            fields=[
                ('catsercod', models.AutoField(db_column='CatSerCod', primary_key=True, serialize=False)),
                ('catsernom', models.CharField(db_column='CatSerNom', max_length=60, unique=True)),
            ],
            options={
                'verbose_name': 'Categoría de Servicio',
                'verbose_name_plural': 'Categorías de Servicios',
                'db_table': 'categoaria_servicio',
            },
        ),
        migrations.CreateModel(
            name='EstadoRegistro',
            fields=[
                ('estregcod', models.AutoField(db_column='EstRegCod', primary_key=True, serialize=False)),
                ('estregnom', models.CharField(db_column='EstRegNom', max_length=100)),
            ],
            options={
                'verbose_name': 'Estado de Registro',
                'verbose_name_plural': 'Estados de Registro',
                'db_table': 'estado_registro',
            },
        ),
        migrations.CreateModel(
            name='TipoConsulta',
            fields=[
                ('tipconcod', models.AutoField(db_column='TipConCod', primary_key=True, serialize=False)),
                ('tipconnom', models.CharField(db_column='TipConNom', max_length=60)),
            ],
            options={
                'verbose_name': 'Tipo de Consulta',
                'verbose_name_plural': 'Tipos de Consulta',
                'db_table': 'tipo_consulta',
            },
        ),
        migrations.CreateModel(
            name='TipoPersonal',
            fields=[
                ('tippercod', models.AutoField(db_column='TipPerCod', primary_key=True, serialize=False)),
                ('tippernom', models.CharField(db_column='TipPerNom', max_length=100)),
            ],
            options={
                'verbose_name': 'Tipo de Personal',
                'verbose_name_plural': 'Tipos de Personal',
                'db_table': 'tipo_personal',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('clidni', models.CharField(db_column='CliDni', max_length=8, primary_key=True, serialize=False)),
                ('clinom', models.CharField(db_column='CliNom', max_length=60)),
                ('cliape', models.CharField(db_column='CliApe', max_length=60)),
                ('clitel', models.CharField(blank=True, db_column='CliTel', max_length=9, null=True)),
                ('clidir', models.CharField(blank=True, db_column='CliDir', max_length=150, null=True)),
                ('cliusu', models.CharField(db_column='CliUsu', max_length=60, unique=True)),
                ('clicon', models.CharField(db_column='CliCon', max_length=255)),
                ('clicor', models.CharField(blank=True, db_column='CliCor', max_length=60, null=True)),
                ('clifecreg', models.DateField(blank=True, db_column='CliFecReg', null=True)),
                ('estregcod', models.ForeignKey(db_column='EstRegCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.estadoregistro')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('perdni', models.CharField(db_column='PerDni', max_length=8, primary_key=True, serialize=False)),
                ('pernom', models.CharField(db_column='PerNom', max_length=60)),
                ('perape', models.CharField(db_column='PerApe', max_length=60)),
                ('pertel', models.CharField(blank=True, db_column='PerTel', max_length=9, null=True)),
                ('perdir', models.CharField(blank=True, db_column='PerDir', max_length=150, null=True)),
                ('perusu', models.CharField(db_column='PerUsu', max_length=60, unique=True)),
                ('percon', models.CharField(db_column='PerCon', max_length=60)),
                ('percor', models.EmailField(blank=True, db_column='PerCor', max_length=254, null=True)),
                ('perfecreg', models.DateField(db_column='PerFecReg')),
                ('estregcod', models.ForeignKey(db_column='EstRegCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.estadoregistro')),
                ('tippercod', models.ForeignKey(db_column='TipPerCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.tipopersonal')),
            ],
            options={
                'verbose_name': 'Personal',
                'verbose_name_plural': 'Personal',
                'db_table': 'personal',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('procod', models.AutoField(db_column='ProCod', primary_key=True, serialize=False)),
                ('pronom', models.CharField(db_column='ProNom', max_length=100, unique=True)),
                ('prodes', models.CharField(blank=True, db_column='ProDes', max_length=500, null=True)),
                ('propreuni', models.DecimalField(db_column='ProPreUni', decimal_places=2, max_digits=10)),
                ('proima', models.CharField(blank=True, db_column='ProImaUrl', default='', max_length=400, null=True)),
                ('proimg', models.ImageField(blank=True, db_column='ProImaPmg', null=True, upload_to='images/')),
                ('catprocod', models.ForeignKey(db_column='CatProCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.categoariaproducto')),
                ('estregcod', models.ForeignKey(db_column='EstRegCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.estadoregistro')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'producto',
            },
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('invcod', models.AutoField(db_column='InvCod', primary_key=True, serialize=False)),
                ('invcan', models.IntegerField(db_column='InvCan')),
                ('invfecing', models.DateField(db_column='InvFecIng')),
                ('procod', models.ForeignKey(db_column='ProCod', on_delete=django.db.models.deletion.CASCADE, to='tienda.producto')),
            ],
            options={
                'verbose_name': 'Inventario',
                'verbose_name_plural': 'Inventarios',
                'db_table': 'inventario',
            },
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
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('sercod', models.AutoField(db_column='SerCod', primary_key=True, serialize=False)),
                ('sernom', models.CharField(db_column='SerNom', max_length=100, unique=True)),
                ('serdes', models.CharField(blank=True, db_column='SerDes', max_length=400, null=True)),
                ('serreqpre', models.CharField(blank=True, db_column='SerReqPre', max_length=45, null=True)),
                ('serdur', models.CharField(blank=True, db_column='SerDur', max_length=60, null=True)),
                ('sercos', models.CharField(db_column='SerCos', max_length=45)),
                ('serima', models.CharField(db_column='SerImaUrl', default='', max_length=400, null=True)),
                ('serimg', models.ImageField(blank=True, db_column='SerImaPng', null=True, upload_to='static/images/')),
                ('categoaria_servicio_catsercod', models.ForeignKey(db_column='CATEGOARIA_SERVICIO_CatSerCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.categoariaservicio')),
                ('estado_registro_estregcod', models.ForeignKey(db_column='ESTADO_REGISTRO_EstRegCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.estadoregistro')),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
                'db_table': 'servicio',
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('evecod', models.AutoField(db_column='EveCod', primary_key=True, serialize=False)),
                ('evedes', models.CharField(blank=True, db_column='EveDes', max_length=150, null=True)),
                ('evefec', models.DateField(db_column='EveFec')),
                ('clidni', models.ForeignKey(db_column='CliDni', on_delete=django.db.models.deletion.CASCADE, to='tienda.cliente')),
                ('perdni', models.ForeignKey(db_column='PerDni', on_delete=django.db.models.deletion.PROTECT, to='tienda.personal')),
                ('sercod', models.ForeignKey(db_column='SerCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.servicio')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'db_table': 'evento',
            },
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('concod', models.AutoField(db_column='ConCod', primary_key=True, serialize=False)),
                ('conpre', models.TextField(db_column='ConPre')),
                ('conres', models.TextField(blank=True, db_column='ConRes', null=True)),
                ('confec', models.DateField(db_column='ConFec', default=datetime.date.today)),
                ('clidni', models.ForeignKey(db_column='CliDNI', on_delete=django.db.models.deletion.PROTECT, to='tienda.cliente')),
                ('perdni', models.ForeignKey(blank=True, db_column='PerDNI', null=True, on_delete=django.db.models.deletion.PROTECT, to='tienda.personal')),
                ('tipconcod', models.ForeignKey(db_column='TipConCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.tipoconsulta')),
            ],
            options={
                'verbose_name': 'Consulta',
                'verbose_name_plural': 'Consultas',
                'db_table': 'consulta',
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('vencod', models.AutoField(db_column='VenCod', primary_key=True, serialize=False)),
                ('vencan', models.IntegerField(db_column='VenCan')),
                ('venprotot', models.DecimalField(db_column='VenProTot', decimal_places=2, max_digits=10)),
                ('venfecres', models.DateField(db_column='VenFecRes')),
                ('venclicod', models.ForeignKey(db_column='VenCliCod', on_delete=django.db.models.deletion.CASCADE, to='tienda.cliente')),
                ('veninvcod', models.ForeignKey(db_column='VenInvCod', on_delete=django.db.models.deletion.PROTECT, to='tienda.inventario')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'db_table': 'venta',
            },
        ),
    ]
