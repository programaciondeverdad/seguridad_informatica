from django.db import models

# Create your models here.
class ValidacionCodigo(models.Model):
    codigo = models.CharField(max_length=8,blank=True, null=True)
    codigo_ingresado = models.CharField(max_length=8, blank=True, null=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    date_init = models.DateField(blank=True, null=True)
