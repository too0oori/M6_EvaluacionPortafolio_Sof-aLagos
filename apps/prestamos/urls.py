from django.urls import path
from . import views
from .views import MisPrestamosView, MisReservasView, SolicitarPrestamoView, RenovarPrestamoView, CancelarReservaView, ReservarLibroView, GestionPrestamosView, GestionReservasView, MarcarDevueltoView

app_name = 'prestamos'

urlpatterns = [
    path('mis_prestamos/', MisPrestamosView.as_view(), name='mis_prestamos'),
    path('solicitar_prestamo/<int:libro_id>/', SolicitarPrestamoView.as_view(), name='solicitar_prestamo'),
    path('renovar_prestamo/<int:prestamo_id>/', RenovarPrestamoView.as_view(), name='renovar_prestamo'),
    path('reservar_libro/<int:libro_id>/', ReservarLibroView.as_view(), name='reservar_libro'),
    path('mis_reservas/', MisReservasView.as_view(), name='mis_reservas'),
    path('cancelar_reserva/<int:reserva_id>/', CancelarReservaView.as_view(), name='cancelar_reserva'),
    path('gestion/', GestionPrestamosView.as_view(), name='gestion_prestamos'),
    path('gestion/reservas/', GestionReservasView.as_view(), name='gestion_reservas'),
    path('marcar_devuelto/<int:prestamo_id>/', MarcarDevueltoView.as_view(), name='marcar_devuelto'),
]