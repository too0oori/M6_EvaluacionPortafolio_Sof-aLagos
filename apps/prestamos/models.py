from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

class Prestamo(models.Model):
    usuario = models.ForeignKey('usuarios.PerfilUsuario', on_delete=models.CASCADE)
    libro = models.ForeignKey('catalogo.Libro', on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('retrasado', 'Retrasado'),
    ], default='activo')

    def clean(self):
        # Verificar si el libro tiene copias disponibles
        if self.libro.copias_disponibles <= 0:
            raise ValidationError("No hay copias disponibles para este libro.")
        
        # Verificar si el libro ya tiene un préstamo activo
        if Prestamo.objects.filter(libro=self.libro, estado='activo').exists():
            raise ValidationError("El libro ya tiene un préstamo activo.")
        
        if self.fecha_devolucion is not None:
                if self.fecha_devolucion < timezone.now().date():
                    raise ValidationError("La fecha de devolución no puede ser anterior a la fecha actual.")
            
        prestamos_activos = Prestamo.objects.filter(libro=self.libro, estado='activo').count()
        if prestamos_activos >= 3:
            raise ValidationError("El usuario ya tiene el máximo permitido de préstamos activos (3).")
        
    def save(self, *args, **kwargs):
        """Guardar y actualizar copias disponibles"""

        # Establecer fecha de devolución si no existe (14 días desde hoy)
        if self.pk is None and self.fecha_devolucion is None:
            self.fecha_devolucion = timezone.now().date() + timedelta(days=14)

        # Solo validar al crear
        if self.pk is None:
            self.full_clean()
            # Guardar el préstamo
            super().save(*args, **kwargs)

        # Si se crea por primera vez, resta una copia del libro
            if self.estado == 'activo':
                self.libro.copias_disponibles = max(self.libro.copias_disponibles - 1, 0)
                self.libro.save()
            
            else:
                # Si ya existe, solo guardar
                super().save(*args, **kwargs)


    def __str__(self):
        return f"Préstamo de {self.libro.titulo} a {self.usuario.usuario.username}"

    class Meta:
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'


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
        return f'Reserva de {self.libro.titulo} por {self.usuario.usuario.username}'

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
