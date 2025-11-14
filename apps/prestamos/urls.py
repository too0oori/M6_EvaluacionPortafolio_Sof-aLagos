from django.urls import path
from . import views
from .views import MisPrestamosView, MisReservasView, SolicitarPrestamoView, DevolverLibroView, HistorialPrestamosView, RenovarPrestamoView, CancelarReservaView, ReservarLibroView   

app_name = 'prestamos'

urlpatterns = [
    path('mis_prestamos/', MisPrestamosView.as_view(), name='mis_prestamos'),
    path('reservar_libro/<int:libro_id>/', ReservarLibroView.as_view(), name='reservar_libro'),  # 👈 corregido
    path('solicitar_prestamo/<int:libro_id>/', SolicitarPrestamoView.as_view(), name='solicitar_prestamo'),
    path('devolver_libro/<int:libro_id>/', DevolverLibroView.as_view(), name='devolver_libro'),
    path('historial_prestamos/', HistorialPrestamosView.as_view(), name='historial_prestamos'),
    path('renovar_prestamo/<int:prestamo_id>/', RenovarPrestamoView.as_view(), name='renovar_prestamo'),
    path('mis_reservas/', MisReservasView.as_view(), name='mis_reservas'),
    path('cancelar_reserva/<int:reserva_id>/', CancelarReservaView.as_view(), name='cancelar_reserva'),
]