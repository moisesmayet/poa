from django.db import models
from django.utils import timezone
from authentication.models import CustomUser


class TipoNotificacion(models.Model):
    tipo_code = models.CharField(max_length=3, unique=True, null=False, verbose_name='Código')
    tipo_name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')

    def delete(self, *args, **kwargs):
        super(TipoNotificacion, self).delete(*args, **kwargs)

    def __str__(self):
        return self.tipo_name

    class Meta:
        db_table = 'TipoNotificacion'
        verbose_name = 'TipoNotificacion'
        verbose_name_plural = 'TipoNotificaciones'
        ordering = ['id']


class Notificacion(models.Model):
    notificacion_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='user_receiver')
    notificacion_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='user_sender')
    notificacion_type = models.ForeignKey(TipoNotificacion, on_delete=models.CASCADE, null=True, verbose_name='Tipo')
    notificacion_message = models.CharField(max_length=250, null=False, verbose_name='Mensaje')
    notificacion_read = models.BooleanField(default=False, verbose_name='Leído')
    notificacion_discharge = models.DateTimeField(null=False, default=timezone.now, verbose_name='Fecha envío')

    def delete(self, *args, **kwargs):
        super(Notificacion, self).delete(*args, **kwargs)

    def __str__(self):
        return self.notificacion_message

    class Meta:
        db_table = 'Notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['notificacion_discharge']


class Parametro(models.Model):
    parametro_name = models.CharField(max_length=40, unique=True, null=False, verbose_name='Nombre del Parámetro')
    parametro_value = models.CharField(max_length=100, null=False, verbose_name='Valor del Parámetro')

    def delete(self, *args, **kwargs):
        super(Parametro, self).delete(*args, **kwargs)

    def __str__(self):
        return self.parametro_name

    class Meta:
        db_table = 'Parametro'
        verbose_name = 'Parámetros'
        verbose_name_plural = 'Parámetros'
        ordering = ['parametro_name']
