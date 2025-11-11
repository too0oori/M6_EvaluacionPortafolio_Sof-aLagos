from django.db import models

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)