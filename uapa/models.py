from django.db import models
from authentication.models import CustomUser


class Sede(models.Model):
    sede_name = models.CharField(max_length=100, null=False, verbose_name='Sede')

    def delete(self, *args, **kwargs):
        super(Sede, self).delete(*args, **kwargs)

    def __str__(self):
        return self.sede_name

    class Meta:
        db_table = 'Sede'
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'
        ordering = ['id']


class TipoEstamento(models.Model):
    tipo_code = models.CharField(max_length=3, unique=True, null=False, verbose_name='Código')
    tipo_name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')
    tipo_cargo = models.CharField(max_length=100, unique=True, null=False, verbose_name='Cargo')
    tipo_faicon = models.CharField(max_length=100, null=True, default='', verbose_name='Fa Icon')

    def delete(self, *args, **kwargs):
        super(TipoEstamento, self).delete(*args, **kwargs)

    def __str__(self):
        return self.tipo_name

    class Meta:
        db_table = 'TipoEstamento'
        verbose_name = 'TipoEstamento'
        verbose_name_plural = 'TipoEstamentos'
        ordering = ['id']


class Estamento(models.Model):
    estamento_name = models.CharField(max_length=100, null=False, verbose_name='Nombre')
    estamento_sede = models.ForeignKey(Sede, on_delete=models.CASCADE, null=False, verbose_name='Sede')
    estamento_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, verbose_name='Vicerrector(a)')
    estamento_tipo = models.ForeignKey(TipoEstamento, on_delete=models.CASCADE, null=True, verbose_name='Tipo')
    estamento_sub = models.ForeignKey('self', on_delete=models.CASCADE, null=True, verbose_name='Estamento Subordinado')
    estamento_has_poa = models.BooleanField(default=False, verbose_name='Tiene POA')
    estamento_roots = models.TextField(null=False, default='', verbose_name='Lista de roots')

    def delete(self, *args, **kwargs):
        super(Estamento, self).delete(*args, **kwargs)

    def __str__(self):
        return self.estamento_name

    class Meta:
        unique_together = (('estamento_name', 'estamento_sede'),)
        db_table = 'Estamento'
        verbose_name = 'Estamento'
        verbose_name_plural = 'Estamentos'
        ordering = ['estamento_name']


class Colaborador(models.Model):
    colaborador_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, verbose_name='Colaborador')
    colaborador_estamento = models.ForeignKey(Estamento, on_delete=models.CASCADE, null=False, verbose_name='Estamento')
    colaborador_can_edit = models.BooleanField(default=False, verbose_name='Puede editar')

    def delete(self, *args, **kwargs):
        super(Colaborador, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.colaborador_user)

    class Meta:
        db_table = 'Colaborador'
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'
        ordering = ['colaborador_estamento']

        constraints = [
            models.UniqueConstraint(fields=['colaborador_user', 'colaborador_estamento'], name='unique_colaborador')
        ]


class Tableau(models.Model):
    tableau_title = models.CharField(max_length=100, null=True, verbose_name='Título')
    tableau_description = models.TextField(null=False, verbose_name='Descripción')
    tableau_url = models.TextField(null=False, verbose_name='URL')
    tableau_anno = models.IntegerField(default=0, null=True, verbose_name='Año')

    def delete(self, *args, **kwargs):
        super(Tableau, self).delete(*args, **kwargs)

    def __str__(self):
        return self.tableau_title

    class Meta:
        db_table = 'Tableau'
        verbose_name = 'Tableau'
        verbose_name_plural = 'Tableau'
        ordering = ['tableau_title']


class TableauEstamento(models.Model):
    tablero_tableau = models.ForeignKey(Tableau, on_delete=models.CASCADE, null=False, verbose_name='Tablero')
    tablero_estamento = models.ForeignKey(Estamento, on_delete=models.CASCADE, null=False, verbose_name='Estamento')

    def delete(self, *args, **kwargs):
        super(TableauEstamento, self).delete(*args, **kwargs)

    def __str__(self):
        return self.tablero_tableau

    class Meta:
        db_table = 'TableauEstamento'
        verbose_name = 'TableauEstamento'
        verbose_name_plural = 'TableauEstamento'
        ordering = ['tablero_tableau']
