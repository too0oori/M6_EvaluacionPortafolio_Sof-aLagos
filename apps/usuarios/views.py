from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistroForm, PerfilForm
from apps.prestamos.models import Prestamo, Reserva
from apps.usuarios.models import PerfilUsuario

class LoginUsuarioView(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True

class RegistroUsuarioView(CreateView, View):
    model = User
    template_name = "auth/registro.html"
    form_class = RegistroForm
    success_url = reverse_lazy("usuarios:login")  # redirige al login tras registrarse

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    """
    Vista de logout que requiere autenticación.
    Redirige a la página de login después de cerrar sesión.
    """
    next_page = reverse_lazy('usuarios:login')

class PerfilUsuarioView(LoginRequiredMixin, DetailView):
    """
    Vista para ver el perfil del usuario actual.
    """
    model = User
    template_name = "usuarios/perfil.html"
    context_object_name = 'user'
    
    def get_object(self):
        """
        Retorna el usuario actual (no el perfil)
        """
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Crear perfil si no existe
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=self.request.user
        )
        
        if created:
            print(f"✓ Perfil creado para el usuario {self.request.user.username}")
        
        # Agregar formulario de perfil
        context['perfil_form'] = PerfilForm(instance=perfil)
        context['perfil'] = perfil  # Agregar el perfil al contexto
        
        # Contar TODOS los préstamos del usuario
        context['total_prestamos'] = Prestamo.objects.filter(
            usuario=perfil
        ).count()
        
        # Contar solo préstamos ACTIVOS
        context['prestamos_activos'] = Prestamo.objects.filter(
            usuario=perfil,
            estado='activo'
        ).count()
        
        # Contar préstamos VENCIDOS
        context['prestamos_vencidos'] = Prestamo.objects.filter(
            usuario=perfil,
            estado='vencido'
        ).count()
        
        # Contar préstamos DEVUELTOS
        context['prestamos_devueltos'] = Prestamo.objects.filter(
            usuario=perfil,
            estado='devuelto'
        ).count()
        
        # Contar TODAS las reservas
        context['total_reservas'] = Reserva.objects.filter(
            usuario=perfil
        ).count()
        
        # Contar reservas PENDIENTES
        context['reservas_pendientes'] = Reserva.objects.filter(
            usuario=perfil,
            estado='pendiente'
        ).count()
        
        return context



class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = PerfilForm
    template_name = "usuarios/editar_perfil.html"
    success_url = reverse_lazy("usuarios:perfil")

    def get_object(self):
        return self.request.user

class CambiarContrasenaView(LoginRequiredMixin, PasswordChangeView):
    template_name = "usuarios/cambiar_contrasena.html"
    success_url = reverse_lazy("usuarios:perfil")