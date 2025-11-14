from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import redirect, render
from apps.prestamos.mixins import LoginRequiredMixin, AdminRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404
from apps.catalogo.models import Libro
from apps.prestamos.models import Prestamo
from apps.usuarios.models import PerfilUsuario



class SolicitarPrestamoView(LoginRequiredMixin, View):
    def post(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)

        # Obtener perfil de usuario
        perfil = PerfilUsuario.objects.get(usuario=request.user)

        # Validar disponibilidad
        if libro.copias_disponibles <= 0:
            messages.error(request, "No hay copias disponibles.")
            return redirect('catalogo:detalle_libro', libro_id=libro.id)

        # Crear préstamo
        prestamo = Prestamo.objects.create(
            usuario=perfil,
            libro=libro,
            fecha_prestamo=timezone.now(),
            fecha_devolucion=timezone.now() + timedelta(days=14),
            estado='activo'
        )

        # Actualizar copias disponibles
        libro.copias_disponibles -= 1
        libro.save()

        # Confirmación
        messages.success(request, "El libro ha sido añadido a tus préstamos.")
        return redirect('prestamos:mis_prestamos')

class MisPrestamosView(LoginRequiredMixin, View):
    # Lógica para ver los préstamos del usuario
    template_name = 'prestamos/mis_prestamos.html'

    def get(self, request):
        prestamos = Prestamo.objects.filter(usuario=request.user.perfilusuario)
        return render(request, self.template_name, {'prestamos': prestamos})

class HistorialPrestamosView(LoginRequiredMixin, View):
    # Lógica para ver el historial de préstamos
    def get(self, request):
        return render(request, 'prestamos/historial.html')

class RenovarPrestamoView(LoginRequiredMixin, View):
    def post(self, request, prestamo_id):
        # Obtener el perfil del usuario actual
        perfil = PerfilUsuario.objects.get(usuario=request.user)

        # Obtener el préstamo perteneciente al perfil
        prestamo = get_object_or_404(Prestamo, id=prestamo_id, usuario=perfil)

        # Sumar 14 días
        prestamo.fecha_devolucion += timedelta(days=14)
        prestamo.save()

        messages.success(request, "Has renovado tu préstamo por 14 días más.")
        return redirect('prestamos:mis_prestamos')

class DevolverLibroView(LoginRequiredMixin, View):
    # Lógica para devolver un libro
    def get(self, request, prestamo_id):
        return render(request, 'prestamos/devolver.html', {'prestamo_id': prestamo_id})

class ReservarLibroView(LoginRequiredMixin, View):
    
    def get(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        return render(request, self.template_name, {'libro': libro})
    
    def post(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)

        # Crear la reserva (sin reducir copias disponibles hasta que esté lista)
        reserva = Prestamo.objects.create(
            usuario=request.user.perfilusuario,
            libro=libro,
            fecha_prestamo=None,  # Se asigna cuando esté disponible
            fecha_devolucion=None,
            estado='reservado'
        )

        messages.success(request, f'Reserva confirmada para "{libro.titulo}". Te notificaremos cuando esté disponible.')
        return redirect('prestamos:reservar_libro', libro_id=libro.id)

class MisReservasView(LoginRequiredMixin, View):
    # Lógica para ver las reservas del usuario
    def get(self, request):
        return render(request, 'prestamos/mis_reservas.html')

class CancelarReservaView(LoginRequiredMixin, View):
    # Lógica para cancelar una reserva
    def get(self, request, reserva_id):
        return render(request, 'prestamos/cancelar_reserva.html', {'reserva_id': reserva_id})
    
class EliminarPrestamoView(LoginRequiredMixin, AdminRequiredMixin, View):

    def post(self, request, prestamo_id):
        prestamo = get_object_or_404(
            Prestamo,
            id=prestamo_id,
            usuario=request.user.perfilusuario
        )

        libro = prestamo.libro

        prestamo.delete()

        libro.copias_disponibles += 1
        libro.save()

        messages.success(request, "Préstamo eliminado correctamente.")
        return redirect('prestamos:mis_prestamos')