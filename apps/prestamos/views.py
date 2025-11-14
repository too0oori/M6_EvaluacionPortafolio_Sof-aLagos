from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import redirect, render
from apps.prestamos.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404
from apps.catalogo.models import Libro
from apps.prestamos.models import Prestamo
from apps.usuarios.models import PerfilUsuario


class SolicitarPrestamoView(LoginRequiredMixin, View):
    # Lógica para solicitar un préstamo
    template_name = 'prestamos/solicitar_prestamo.html'
    
    def get(self, request, libro_id):
        # Mostrar la página de confirmación antes de solicitar
        libro = get_object_or_404(Libro, id=libro_id)
        return render(request, self.template_name, {'libro': libro})
    
    def post(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        perfil = request.user.perfilusuario

        # Validar disponibilidad
        if libro.copias_disponibles > 0:
            # Crear el préstamo
            prestamo = Prestamo.objects.create(
                usuario=perfil,
                libro=libro,
                fecha_prestamo=timezone.now(),
                fecha_devolucion=timezone.now() + timedelta(days=14),
                estado='activo'
            )
            # Actualizar las copias disponibles del libro
            libro.copias_disponibles -= 1
            libro.save()

            messages.success(request, f'¡Préstamo confirmado! Tienes "{libro.titulo}" hasta el {prestamo.fecha_devolucion.strftime("%d/%m/%Y")}')
            return redirect('catalogo:detalle_libro', libro_id=libro.id)
        else:
            messages.error(request, 'Lo sentimos, no hay copias disponibles de este libro.')
            return redirect('catalogo:detalle_libro', libro_id=libro.id)
    
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
    # Lógica para renovar un préstamo
    def get(self, request, prestamo_id):
        return render(request, 'prestamos/renovar.html', {'prestamo_id': prestamo_id})

class DevolverLibroView(LoginRequiredMixin, View):
    # Lógica para devolver un libro
    def get(self, request, prestamo_id):
        return render(request, 'prestamos/devolver.html', {'prestamo_id': prestamo_id})

class ReservarLibroView(LoginRequiredMixin, View):
    template_name = 'prestamos/reservar_libro.html'
    
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