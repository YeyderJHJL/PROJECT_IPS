import datetime
from django.db import models
from django.contrib.auth.models import User

# GENERAL ################################################

class EstadoRegistro(models.Model):
    estregcod = models.AutoField(db_column='EstRegCod', primary_key=True)
    estregnom = models.CharField(db_column='EstRegNom', max_length=100)

    class Meta:
        db_table = 'estado_registro'
        verbose_name = 'Estado de Registro'
        verbose_name_plural = 'Estados de Registro'

    def __str__(self):
        return self.estregnom

# PERSONAL ################################################

class TipoPersonal(models.Model):
    tippercod = models.AutoField(db_column='TipPerCod', primary_key=True)
    tippernom = models.CharField(db_column='TipPerNom', max_length=100)

    class Meta:
        db_table = 'tipo_personal'
        verbose_name = 'Tipo de Personal'
        verbose_name_plural = 'Tipos de Personal'

    def __str__(self):
        return self.tippernom

class Personal(models.Model):
    perdni = models.CharField(db_column='PerDni', primary_key=True, max_length=8)
    pernom = models.CharField(db_column='PerNom', max_length=60)
    perape = models.CharField(db_column='PerApe', max_length=60)
    pertel = models.CharField(db_column='PerTel', max_length=9, blank=True, null=True)
    perdir = models.CharField(db_column='PerDir', max_length=150, blank=True, null=True)
    perusu = models.CharField(db_column='PerUsu', unique=True, max_length=60)
    percon = models.CharField(db_column='PerCon', max_length=1000)
    percor = models.EmailField(db_column='PerCor', blank=True, null=True)  # Cambiado a EmailField para correos
    perfecreg = models.DateField(db_column='PerFecReg')
    estregcod = models.ForeignKey(EstadoRegistro, models.PROTECT, db_column='EstRegCod')
    tippercod = models.ForeignKey(TipoPersonal, models.PROTECT, db_column='TipPerCod')

    class Meta:
        db_table = 'personal'
        verbose_name = 'Personal'
        verbose_name_plural = 'Personal'

    def __str__(self):
        return f"{self.pernom} {self.perape}"

# CLIENTE ################################################

class Cliente(models.Model):
    clidni = models.CharField(db_column='CliDni', primary_key=True, max_length=8)
    clinom = models.CharField(db_column='CliNom', max_length=60)
    cliape = models.CharField(db_column='CliApe', max_length=60)
    clitel = models.CharField(db_column='CliTel', max_length=9, blank=True, null=True)
    clidir = models.CharField(db_column='CliDir', max_length=150, blank=True, null=True)
    cliusu = models.CharField(db_column='CliUsu', unique=True, max_length=60)
    clicon = models.CharField(db_column='CliCon', max_length=500)
    clicor = models.CharField(db_column='CliCor', max_length=60, blank=True, null=True)
    clifecreg = models.DateField(db_column='CliFecReg', blank=True, null=True)
    estregcod = models.ForeignKey(EstadoRegistro, models.PROTECT, db_column='EstRegCod')

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return f"{self.clinom} {self.cliape}"

# PRODUCTO ################################################

class CategoariaProducto(models.Model):
    catprocod = models.AutoField(db_column='CatProCod', primary_key=True)
    catpronom = models.CharField(db_column='CatProNom', unique=True, max_length=60)

    class Meta:
        db_table = 'categoaria_producto'
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Productos'

    def __str__(self):
        return self.catpronom

class Producto(models.Model):
    procod = models.AutoField(db_column='ProCod', primary_key=True)
    pronom = models.CharField(db_column='ProNom', unique=True, max_length=100)
    prodes = models.CharField(db_column='ProDes', max_length=500, blank=True, null=True)
    propreuni = models.DecimalField(db_column='ProPreUni', max_digits=10, decimal_places=2)
    estregcod = models.ForeignKey(EstadoRegistro, models.PROTECT, db_column='EstRegCod')
    catprocod = models.ForeignKey(CategoariaProducto, models.PROTECT, db_column='CatProCod')
    proima = models.CharField(db_column='ProImaUrl', max_length=400, default='', blank=True, null=True)
    proimg = models.ImageField(upload_to='images/', blank=True, null=True, db_column='ProImaPmg')

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.pronom

class Inventario(models.Model):
    invcod = models.AutoField(db_column='InvCod', primary_key=True)
    invcan = models.IntegerField(db_column='InvCan')
    invfecing = models.DateField(db_column='InvFecIng')
    procod = models.ForeignKey(Producto, models.CASCADE, db_column='ProCod')

    class Meta:
        db_table = 'inventario'
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return f"Inventario {self.invcod} - {self.procod}"

class Venta(models.Model):
    vencod = models.AutoField(db_column='VenCod', primary_key=True)
    vencan = models.IntegerField(db_column='VenCan')
    venprotot = models.DecimalField(db_column='VenProTot', max_digits=10, decimal_places=2)
    venfecres = models.DateField(db_column='VenFecRes')
    venclicod = models.ForeignKey(Cliente, models.CASCADE, db_column='VenCliCod')
    veninvcod = models.ForeignKey(Inventario, models.PROTECT, db_column='VenInvCod')

    class Meta:
        db_table = 'venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"Venta {self.vencod} - {self.venfecres}"

class EventoProducto(models.Model):
    evecod = models.AutoField(primary_key=True)
    evedes = models.CharField(max_length=150, blank=True, null=True)
    evefec = models.DateField()
    procod = models.ForeignKey(Producto, models.PROTECT, db_column='ProCod')
    cantidad = models.PositiveIntegerField()
    cliente = models.ForeignKey('Cliente', models.CASCADE, db_column='CliDni', null=True)  
    notas = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'evento_producto'
        verbose_name = 'Evento de Producto'
        verbose_name_plural = 'Eventos de Productos'

    def __str__(self):
        return f"Evento {self.evecod} - {self.evefec}"
    
# SERVICIO ################################################

class CategoariaServicio(models.Model):
    catsercod = models.AutoField(db_column='CatSerCod', primary_key=True)
    catsernom = models.CharField(db_column='CatSerNom', unique=True, max_length=60)

    class Meta:
        db_table = 'categoaria_servicio'
        verbose_name = 'Categoría de Servicio'
        verbose_name_plural = 'Categorías de Servicios'

    def __str__(self):
        return self.catsernom

class Servicio(models.Model):
    sercod = models.AutoField(db_column='SerCod', primary_key=True)
    sernom = models.CharField(db_column='SerNom', unique=True, max_length=100)
    serdes = models.CharField(db_column='SerDes', max_length=400, blank=True, null=True)
    serreqpre = models.CharField(db_column='SerReqPre', max_length=45, blank=True, null=True)
    serdur = models.CharField(db_column='SerDur', max_length=60, blank=True, null=True)
    sercos = models.CharField(db_column='SerCos', max_length=45)
    serima = models.CharField(db_column='SerImaUrl', max_length=400, default='', null=True)
    serimg = models.ImageField(upload_to='static/images/', blank=True, null=True, db_column='SerImaPng')
    estado_registro_estregcod = models.ForeignKey(EstadoRegistro, models.PROTECT, db_column='ESTADO_REGISTRO_EstRegCod')
    categoaria_servicio_catsercod = models.ForeignKey(CategoariaServicio, models.PROTECT, db_column='CATEGOARIA_SERVICIO_CatSerCod')

    class Meta:
        db_table = 'servicio'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.sernom

class Evento(models.Model):
    evecod = models.AutoField(db_column='EveCod', primary_key=True)
    evedes = models.CharField(db_column='EveDes', max_length=150, blank=True, null=True)
    evefec = models.DateField(db_column='EveFec')
    sercod = models.ForeignKey(Servicio, models.PROTECT, db_column='SerCod')
    clidni = models.ForeignKey(Cliente, models.CASCADE, db_column='CliDni')
    perdni = models.ForeignKey(Personal, models.PROTECT, db_column='PerDni')

    class Meta:
        db_table = 'evento'
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f"Evento {self.evecod} - {self.evefec}"

# CONSULTA ################################################

class TipoConsulta(models.Model):
    tipconcod = models.AutoField(db_column='TipConCod', primary_key=True)
    tipconnom = models.CharField(db_column='TipConNom', max_length=60)

    class Meta:
        db_table = 'tipo_consulta'
        verbose_name = 'Tipo de Consulta'
        verbose_name_plural = 'Tipos de Consulta'

    def __str__(self):
        return self.tipconnom

class Consulta(models.Model):
    concod = models.AutoField(db_column='ConCod', primary_key=True)  # Campo autogenerado
    conpre = models.TextField(db_column='ConPre')  # Pregunta
    conres = models.TextField(db_column='ConRes', null=True, blank=True)  # Respuesta
    confec = models.DateField(db_column='ConFec', default=datetime.date.today)  # Fecha automática
    clidni = models.ForeignKey('Cliente', models.PROTECT, db_column='CliDNI')  # Cliente
    perdni = models.ForeignKey(Personal, models.PROTECT, db_column='PerDNI', null=True, blank=True)  # Personal
    tipconcod = models.ForeignKey('TipoConsulta', models.PROTECT, db_column='TipConCod')  # Tipo de Consulta
    class Meta:
        db_table = 'consulta'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        return f"Consulta {self.concod}: {self.conpre}"