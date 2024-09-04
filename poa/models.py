
import os
from django.db import models
from django.utils import timezone
from datetime import datetime
from authentication.models import CustomUser
from uapa.models import Estamento


class MedioVerificacion(models.Model):
    medio_description = models.CharField(max_length=100, unique=True, null=False, verbose_name='Medio de Verificación')
    medio_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, verbose_name='Creador')

    def delete(self, *args, **kwargs):
        super(MedioVerificacion, self).delete(*args, **kwargs)

    def __str__(self):
        return self.medio_description

    class Meta:
        unique_together = (('medio_description', 'medio_user'),)
        db_table = 'MedioVerificacion'
        verbose_name = 'Medio de Verificación'
        verbose_name_plural = 'Medios de Verificación'
        ordering = ['medio_description']


class Responsable(models.Model):
    responsable_description = models.CharField(max_length=100, unique=True, null=False, verbose_name='Responsable')
    responsable_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, verbose_name='Creador')

    def delete(self, *args, **kwargs):
        super(Responsable, self).delete(*args, **kwargs)

    def __str__(self):
        return self.responsable_description

    class Meta:
        unique_together = (('responsable_description', 'responsable_user'),)
        db_table = 'Responsable'
        verbose_name = 'Responsable'
        verbose_name_plural = 'Responsables'
        ordering = ['responsable_description']


class POAEstado(models.Model):
    estado_name = models.CharField(max_length=100, null=False, verbose_name='Estado')

    def delete(self, *args, **kwargs):
        super(POAEstado, self).delete(*args, **kwargs)

    def __str__(self):
        return self.estado_name

    class Meta:
        db_table = 'POAEstado'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['estado_name']


class POA(models.Model):
    poa_anno = models.IntegerField(null=False, default=datetime.now().year, verbose_name='Año')
    poa_estamento = models.ForeignKey(Estamento, on_delete=models.CASCADE, null=False, verbose_name='Estamento')
    poa_estado = models.ForeignKey(POAEstado, on_delete=models.CASCADE, null=False, verbose_name='Estado')
    poa_user_modificacion = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, verbose_name='Modificado por')
    poa_fecha_modificacion = models.DateField(null=False, default=timezone.now, verbose_name='Fecha modificación')
    poa_include_subs = models.BooleanField(null=False, default=False, verbose_name='Incluir subordinados')

    def delete(self, *args, **kwargs):
        super(POA, self).delete(*args, **kwargs)

    def __str__(self):
        return self.poa_anno

    class Meta:
        unique_together = (('poa_anno', 'poa_estamento'),)
        db_table = 'POA'
        verbose_name = 'POA'
        verbose_name_plural = 'POA'
        ordering = ['poa_anno']


class Eje(models.Model):
    eje_description = models.TextField(null=False, verbose_name='Eje')

    def delete(self, *args, **kwargs):
        super(Eje, self).delete(*args, **kwargs)

    def __str__(self):
        return self.eje_description

    class Meta:
        db_table = 'Eje'
        verbose_name = 'Eje'
        verbose_name_plural = 'Ejes'
        ordering = ['eje_description']


class Objetivo(models.Model):
    objetivo_description = models.TextField(null=False, verbose_name='Objetivo')
    objetivo_eje = models.ForeignKey(Eje, on_delete=models.CASCADE, null=False, verbose_name='Eje')

    def delete(self, *args, **kwargs):
        super(Objetivo, self).delete(*args, **kwargs)

    def __str__(self):
        return self.objetivo_description

    class Meta:
        db_table = 'Objetivo'
        verbose_name = 'Objetivo'
        verbose_name_plural = 'Objetivos'
        ordering = ['objetivo_description']


class Linea(models.Model):
    linea_description = models.TextField(null=False, verbose_name='Línea de Actuación')
    linea_objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, null=False, verbose_name='Objetivo')

    def delete(self, *args, **kwargs):
        super(Linea, self).delete(*args, **kwargs)

    def __str__(self):
        return self.linea_description

    class Meta:
        db_table = 'Linea'
        verbose_name = 'Línea'
        verbose_name_plural = 'Línea'
        ordering = ['linea_description']


class ObjetivoOperativo(models.Model):
    operativo_poa = models.ForeignKey(POA, on_delete=models.CASCADE, null=False, verbose_name='POA')
    operativo_linea = models.ForeignKey(Linea, on_delete=models.CASCADE, null=False, verbose_name='Linea')
    operativo_description = models.TextField(null=False, verbose_name='Objetivo Operativo')
    operativo_order = models.IntegerField(null=False, default=1, verbose_name='Orden')
    operativo_selected = models.BooleanField(null=False, default=False, verbose_name='Seleccionado')

    def delete(self, *args, **kwargs):
        super(ObjetivoOperativo, self).delete(*args, **kwargs)

    def __str__(self):
        return self.operativo_description

    class Meta:
        unique_together = (('operativo_poa', 'operativo_linea', 'operativo_description'),)
        db_table = 'ObjetivoOperativo'
        verbose_name = 'Objetivo Operativo'
        verbose_name_plural = 'Objetivos Operativos'
        ordering = ['operativo_order']


class Meta(models.Model):
    meta_description = models.TextField(null=False, verbose_name='Meta')
    meta_operativo = models.ForeignKey(ObjetivoOperativo, on_delete=models.CASCADE, null=False, verbose_name='Objetivo Operativo')
    meta_order = models.IntegerField(null=False, default=1, verbose_name='Orden')
    meta_selected = models.BooleanField(null=False, default=False, verbose_name='Seleccionada')

    def delete(self, *args, **kwargs):
        super(Meta, self).delete(*args, **kwargs)

    def __str__(self):
        return self.meta_description

    class Meta:
        db_table = 'Meta'
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'
        ordering = ['meta_order']


class Actividad(models.Model):
    actividad_description = models.TextField(null=False, verbose_name='Actividad')
    actividad_meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=False, verbose_name='Meta')
    actividad_medio = models.ForeignKey(MedioVerificacion, on_delete=models.CASCADE, null=False, verbose_name='Indicador Verificable')
    actividad_responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, null=False, verbose_name='Responsable')
    actividad_presupuesto = models.DecimalField(null=False, default=0, max_digits=15, decimal_places=2, verbose_name='Presupuesto')
    actividad_peso = models.IntegerField(null=False, default=0, verbose_name='Peso')
    actividad_order = models.IntegerField(null=False, default=1, verbose_name='Orden')

    def delete(self, *args, **kwargs):
        super(Actividad, self).delete(*args, **kwargs)

    def __str__(self):
        return self.actividad_description

    class Meta:
        db_table = 'Actividad'
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['actividad_order']


class Mes(models.Model):
    mes_name = models.CharField(max_length=100, null=False, verbose_name='Mes')
    mes_number = models.IntegerField(null=False, verbose_name='Mes')

    def delete(self, *args, **kwargs):
        super(Mes, self).delete(*args, **kwargs)

    def __str__(self):
        return self.mes_number

    class Meta:
        db_table = 'Mes'
        verbose_name = 'Mes'
        verbose_name_plural = 'Meses'
        ordering = ['mes_number']


class Cronograma(models.Model):
    cronograma_actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, null=False, verbose_name='Actividad')
    cronograma_mes = models.ForeignKey(Mes, on_delete=models.CASCADE, null=False, verbose_name='Mes', related_name='cronograma_mes')
    cronograma_cumplimiento = models.BooleanField(null=False, default=False, verbose_name='Cumplimiento')
    cronograma_presupuesto = models.DecimalField(null=False, default=0, max_digits=15, decimal_places=2, verbose_name='Presupuesto Gastado')
    cronograma_notas = models.TextField(null=False, default='', verbose_name='Notas')
    cronograma_cumplimiento_mes = models.ForeignKey(Mes, on_delete=models.CASCADE, default=1, verbose_name='Mes Cumplimiento', related_name='cronograma_cumplimiento_mes')

    def delete(self, *args, **kwargs):
        super(Cronograma, self).delete(*args, **kwargs)

    class Meta:
        unique_together = (('cronograma_actividad', 'cronograma_mes'),)
        db_table = 'Cronograma'
        verbose_name = 'Cronograma'
        verbose_name_plural = 'Cronogramas'
        ordering = ['id']


class Evidencia(models.Model):
    evidencia_description = models.CharField(max_length=100, null=False, verbose_name='Descripción')
    evidencia_file = models.FileField(upload_to='evidencias', null=False, blank=True, verbose_name='Evidencia')
    evidencia_cronograma = models.ForeignKey(Cronograma, on_delete=models.CASCADE, null=False, verbose_name='Cronograma')

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.evidencia_file.path):
            os.remove(self.evidencia_file.path)
        super(Evidencia, self).delete(*args, **kwargs)

    def __str__(self):
        return self.evidencia_description

    class Meta:
        db_table = 'Evidencia'
        verbose_name = 'Evidencia'
        verbose_name_plural = 'Evidencias'
        ordering = ['evidencia_cronograma']


class Nota(models.Model):
    nota_description = models.TextField(null=False, verbose_name='Nota')
    nota_poa = models.ForeignKey(POA, on_delete=models.CASCADE, null=True, verbose_name='POA')
    nota_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, verbose_name='Usuario')
    nota_itemid = models.IntegerField(default=0, null=True, verbose_name='Id')
    nota_itemname = models.CharField(max_length=100, null=True, verbose_name='Nombre')
    nota_date = models.DateTimeField(null=False, default=timezone.now, verbose_name='Fecha')
    nota_checked = models.BooleanField(null=False, default=False, verbose_name='Cumplimiento')

    def delete(self, *args, **kwargs):
        super(Nota, self).delete(*args, **kwargs)

    def __str__(self):
        return self.estado_name

    class Meta:
        db_table = 'Nota'
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['nota_itemname', 'nota_date']


class Noticia(models.Model):
    noticia_title = models.CharField(max_length=100, null=True, verbose_name='Título')
    noticia_description = models.TextField(null=False, verbose_name='Descripción')
    noticia_start = models.DateField(null=False, default=timezone.now, verbose_name='Fecha inicio')
    noticia_end = models.DateField(null=False, default=timezone.now, verbose_name='Fecha inicio')
    noticia_always = models.BooleanField(null=False, default=False, verbose_name='Mostrar siempre')

    def delete(self, *args, **kwargs):
        super(Noticia, self).delete(*args, **kwargs)

    def __str__(self):
        return self.noticia_title

    class Meta:
        db_table = 'Noticia'
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['noticia_start']


class Log(models.Model):
    log_poa = models.IntegerField(default=0, null=True, verbose_name='POA')
    log_poaname = models.TextField(default='', null=True, verbose_name='POA')
    log_user = models.IntegerField(default=0, null=False, verbose_name='Usuario')
    log_username = models.TextField(default='', null=False, verbose_name='Usuario')
    log_date = models.DateTimeField(null=False, default=timezone.now, verbose_name='Fecha')
    log_action = models.CharField(max_length=100, default='', verbose_name='Acción')
    log_description = models.TextField(null=False, verbose_name='Descripción')

    def delete(self, *args, **kwargs):
        super(Log, self).delete(*args, **kwargs)

    def __str__(self):
        return self.log_description

    class Meta:
        db_table = 'Log'
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        ordering = ['log_date']


class Bug(models.Model):
    bug_poa = models.IntegerField(default=0, null=True, verbose_name='POA')
    bug_poaname = models.TextField(default='', null=True, verbose_name='POA')
    bug_user = models.IntegerField(default=0, null=False, verbose_name='Usuario')
    bug_username = models.TextField(default='', null=False, verbose_name='Usuario')
    bug_date = models.DateTimeField(null=False, default=timezone.now, verbose_name='Fecha')
    bug_origin = models.CharField(max_length=100, null=False, verbose_name='Origen')
    bug_description = models.TextField(null=False, verbose_name='Descripción')

    def delete(self, *args, **kwargs):
        super(Bug, self).delete(*args, **kwargs)

    def __str__(self):
        return self.bug_description

    class Meta:
        db_table = 'Bug'
        verbose_name = 'Bug'
        verbose_name_plural = 'Bugs'
        ordering = ['bug_date']
