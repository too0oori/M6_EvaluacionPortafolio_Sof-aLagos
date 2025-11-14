from datetime import timedelta, timezone
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from apps.prestamos.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404
from apps.catalogo.models import Libro
from apps.prestamos.models import Prestamo


class SolicitarPrestamoView(LoginRequiredMixin, View):
    # Lógica para solicitar un préstamo
    def post(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)

        #se valida disponibilidad
        if libro.copias_disponibles > 0:
            return redirect('catalogo:detalle_libro', libro_id=libro.id)
        
        # Crear el préstamo
        prestamo = Prestamo.objects.create(
            usuario=request.user,
            libro=libro,
            fecha_prestamo=timezone.now(),
            fecha_devolucion=timezone.now() + timedelta(days=14),
            estado='activo'
        )
        # Actualizar las copias disponibles del libro
        libro.copias_disponibles -= 1
        libro.save()

        # Redirigir al detalle del libro
        messages.success(request, 'Libro añadido a tus préstamos exitosamente.')
        return redirect('catalogo:detalle_libro', libro_id=libro.id)
class MisPrestamosView(LoginRequiredMixin, View):
    # Lógica para ver los préstamos del usuario
    def get(self, request):
        return render(request, 'prestamos/mis_prestamos.html')

class HistorialPrestamosView(LoginRequiredMixin, View):
    # Lógica para ver el historial de préstamos
    def get(self, request):
        return render(request, 'prestamos/historial.html')

class RenovarPrestamoView(LoginRequiredMixin, View):
    # Lógica para renovar un préstamo
    def get(self, request, prestamo_id):
        return render(request, 'prestamos/renovar.html', {'prestamo_id': prestamo_id})

class DevolverLibroView(LoginRequiredMixin, View):
    # Lógica para devolver un libro
    def get(self, request, prestamo_id):
        return render(request, 'prestamos/devolver.html', {'prestamo_id': prestamo_id})

class ReservarLibroView(LoginRequiredMixin, View):
    # Lógica para reservar un libro
    def get(self, request, libro_id):
        return render(request, 'prestamos/reservar.html', {'libro_id': libro_id})

class MisReservasView(LoginRequiredMixin, View):
    # Lógica para ver las reservas del usuario
    def get(self, request):
        return render(request, 'prestamos/mis_reservas.html')

class CancelarReservaView(LoginRequiredMixin, View):
    # Lógica para cancelar una reserva
    def get(self, request, reserva_id):
        return render(request, 'prestamos/cancelar_reserva.html', {'reserva_id': reserva_id})