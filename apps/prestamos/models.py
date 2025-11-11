from django.db import models

class Prestamo(models.Model):
    usuario = models.ForeignKey('usuarios.PerfilUsuario', on_delete=models.CASCADE)
    libro = models.ForeignKey('catalogo.Libro', on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('prestado', 'Prestado'),
        ('devuelto', 'Devuelto'),
        ('retrasado', 'Retrasado'),
    ], default='prestado')

    def __str__(self):
        return f'Préstamo de {self.libro.titulo} a {self.usuario.username}'

    class Meta:
        verbose_name = 'Prestamo'
        verbose_name_plural = 'Prestamos'

class Reserva(models.Model):
    usuario = models.ForeignKey('usuarios.PerfilUsuario', on_delete=models.CASCADE)
    libro = models.ForeignKey('catalogo.Libro', on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('cumplida', 'Cumplida'),
        ('cancelada', 'Cancelada'),
    ], default='pendiente')

    def __str__(self):
        return f'Reserva de {self.libro.titulo} por {self.usuario.username}'

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'