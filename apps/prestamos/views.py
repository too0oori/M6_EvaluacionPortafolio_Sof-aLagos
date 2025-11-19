from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from apps.core.mixins import LoginRequiredMixin, AdminRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404
from apps.catalogo.models import Libro
from apps.prestamos.models import Prestamo, Reserva
from apps.usuarios.models import PerfilUsuario
from apps.usuarios.forms import PerfilUsuarioForm
from django.core.exceptions import ValidationError


class SolicitarPrestamoView(LoginRequiredMixin, View):
        
    def post(self, request, libro_id):
        perfil = request.user.perfilusuario
        
        prestamos_activos = Prestamo.objects.filter(
            usuario=perfil, estado='activo'
        ).count()
        if prestamos_activos >= 3:
            messages.error(request, "Ya tienes 3 préstamos activos")
            return redirect('catalogo:detalle_libro', libro_id)

        # Creamos el préstamo SIN guardarlo aún
        prestamo = Prestamo(
            usuario=perfil,
            libro=libro,
            fecha_prestamo=timezone.now(),
            estado='activo',
        )

        try:
            prestamo.save()  # esto ejecuta clean() automáticamente
            messages.success(request, f"✔ Préstamo creado para '{libro.titulo}'.")
        except ValidationError as e:
            # El ValidationError puede venir con múltiples mensajes
            if hasattr(e, "messages"):
                for error in e.messages:
                    messages.error(request, error)
            else:
                messages.error(request, str(e))
        except Exception:
            messages.error(request, "Ocurrió un error inesperado al procesar tu solicitud.")

        return redirect('detalle_libro', libro_id=libro.id)


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
    

    def post(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)

        # Validar que realmente NO haya copias disponibles
        if libro.copias_disponibles > 0:
            messages.warning(request, 'Este libro tiene copias disponibles. Puedes solicitarlo en préstamo directamente.')
            return redirect('catalogo:detalle_libro', libro_id=libro.id)


        # Verificar que no tenga ya una reserva activa
        reserva_existente = Reserva.objects.filter(
            usuario=request.user.perfilusuario,
            libro=libro,
            estado='pendiente'
        ).exists()
        
        if reserva_existente:
            messages.info(request, 'Ya tienes una reserva activa para este libro.')
            return redirect('prestamos:mis_reservas')
        
        # Crear la reserva
        reserva = Reserva.objects.create(
            usuario=request.user.perfilusuario,
            libro=libro,
            estado='pendiente' 
        )

        messages.success(request, f'Reserva confirmada para "{libro.titulo}". Te notificaremos cuando esté disponible.')
        return redirect('prestamos:mis_reservas')
class MisReservasView(LoginRequiredMixin, View):
    template_name = 'prestamos/mis_reservas.html'
    # Lógica para ver las reservas del usuario
    def get(self, request):
        reservas = Reserva.objects.filter(usuario=request.user.perfilusuario)
        return render(request, self.template_name, {'reservas': reservas})

class CancelarReservaView(LoginRequiredMixin, View):
    # Lógica para cancelar una reserva
    def post(self, request, reserva_id):
        reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user.perfilusuario)
        reserva.delete()
        messages.success(request, "Reserva cancelada correctamente.")
        return redirect('prestamos:mis_reservas')
    
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