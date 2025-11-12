from django.shortcuts import render
from apps.prestamos.mixins import LoginRequiredMixin
from django.views import View


class SolicitarPrestamoView(LoginRequiredMixin, View):
    # Lógica para solicitar un préstamo
    def get(self, request):
        return render(request, 'prestamos/solicitar.html')

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