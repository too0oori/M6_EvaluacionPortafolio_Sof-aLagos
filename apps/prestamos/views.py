from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from apps.core.mixins import LoginRequiredMixin, AdminRequiredMixin, BibliotecarioRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404
from apps.catalogo.models import Libro
from apps.prestamos.models import Prestamo, Reserva
from apps.usuarios.models import PerfilUsuario
from apps.usuarios.forms import PerfilUsuarioForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.views.generic import ListView


class SolicitarPrestamoView(LoginRequiredMixin, View):
        
    def post(self, request, libro_id):
        # Obtener el libro solicitado
        libro = get_object_or_404(Libro, id=libro_id)

        # Obtener o crear perfil
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=request.user
        )
        
        prestamos_activos = Prestamo.objects.filter(
            usuario=perfil, estado='activo'
        ).count()
        if prestamos_activos >= 3:
            messages.error(request, "Ya tienes 3 préstamos activos. Debes devolver uno antes de solicitar otro.")
            return redirect('catalogo:detalle_libro', libro_id=libro.id)
        
        # Verificar disponibilidad
        if libro.copias_disponibles <= 0:
            messages.warning(request, "No hay copias disponibles. Puedes reservar este libro.")
            return redirect('catalogo:detalle_libro', libro_id=libro.id)

       
        # Crear préstamo dentro de una transacción
        try:
            with transaction.atomic():
                prestamo = Prestamo(
                    usuario=perfil,
                    libro=libro,
                    estado='activo',
                )
                prestamo.save()
                
            messages.success(request, f"✔ Préstamo creado para '{libro.titulo}'. Tienes 14 días para devolverlo.")
            
        except ValidationError as e:
            # Manejar errores de validación
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, error)
            elif hasattr(e, 'messages'):
                for error in e.messages:
                    messages.error(request, error)
            else:
                messages.error(request, str(e))
                
        except Exception as e:
            # Error inesperado
            messages.error(request, f"Error inesperado: {str(e)}")
            print(f"Error en SolicitarPrestamoView: {e}")  # Para debugging
            
        return redirect('catalogo:detalle_libro', libro_id=libro.id)



class MisPrestamosView(LoginRequiredMixin, View):
    # Lógica para ver los préstamos del usuario
    template_name = 'prestamos/mis_prestamos.html'

    def get(self, request):

        perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
        
        prestamos = Prestamo.objects.filter(usuario=request.user.perfilusuario)
        return render(request, self.template_name, {'prestamos': prestamos})


class RenovarPrestamoView(LoginRequiredMixin, View):
    def post(self, request, prestamo_id):
        # Obtener el perfil del usuario actual
        perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)

        # Obtener el préstamo perteneciente al perfil
        prestamo = get_object_or_404(Prestamo, id=prestamo_id, usuario=perfil)

        # Sumar 14 días
        prestamo.fecha_devolucion += timedelta(days=14)
        prestamo.save()

        messages.success(request, "Has renovado tu préstamo por 14 días más.")
        return redirect('prestamos:mis_prestamos')

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
    
class GestionPrestamosView(BibliotecarioRequiredMixin, ListView):
    """Vista para que bibliotecarios gestionen préstamos"""
    model = Prestamo
    template_name = 'prestamos/gestion_prestamos.html'
    context_object_name = 'prestamos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Prestamo.objects.select_related(
            'usuario__usuario', 'libro'
        ).order_by('-fecha_prestamo')
    
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_prestamos'] = Prestamo.objects.count()
        context['prestamos_activos'] = Prestamo.objects.filter(estado='activo').count()
        context['prestamos_retrasados'] = Prestamo.objects.filter(estado='retrasado').count()
        return context
    

class GestionReservasView(BibliotecarioRequiredMixin, ListView):
    """Vista para que bibliotecarios gestionen reservas"""
    model = Reserva
    template_name = 'prestamos/gestion_reservas.html'
    context_object_name = 'reservas'
    paginate_by = 20
    
    def get_queryset(self):
        return Reserva.objects.select_related(
            'usuario__usuario', 'libro'
        ).order_by('-fecha_reserva')
class MarcarDevueltoView(BibliotecarioRequiredMixin, View):
    """Marcar préstamo como devuelto"""
    
    def post(self, request, prestamo_id):
        prestamo = get_object_or_404(Prestamo, id=prestamo_id)
        
        if prestamo.estado != 'devuelto':
            prestamo.estado = 'devuelto'
            prestamo.fecha_devolucion = timezone.now().date()
            prestamo.save()
            
            # Devolver copia al libro
            prestamo.libro.copias_disponibles += 1
            prestamo.libro.save()
            
            messages.success(request, f'Préstamo de "{prestamo.libro.titulo}" marcado como devuelto.')
        else:
            messages.info(request, 'Este préstamo ya estaba devuelto.')
        
        return redirect('prestamos:gestion_prestamos')