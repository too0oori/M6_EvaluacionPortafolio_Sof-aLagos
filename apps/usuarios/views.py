from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from apps.core.mixins import LoginRequiredMixin
from .forms import RegistroForm, PerfilUsuarioForm, UserForm
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
    model = User
    template_name = "usuarios/perfil.html"
    context_object_name = 'user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Crear perfil si no existe
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=self.request.user
        )
        

        context['user_form'] = UserForm(instance=self.request.user)
        context['perfil_form'] = PerfilUsuarioForm(instance=perfil)
        context['perfil'] = perfil
        
        # Estadísticas
        context['total_prestamos'] = Prestamo.objects.filter(
            usuario=perfil
        ).count()
        
        context['prestamos_activos'] = Prestamo.objects.filter(
            usuario=perfil,
            estado='activo'
        ).count()
        
        #aggregate para mejor performance
        from django.db.models import Count, Q
        
        stats = Prestamo.objects.filter(usuario=perfil).aggregate(
            total=Count('id'),
            activos=Count('id', filter=Q(estado='activo')),
            devueltos=Count('id', filter=Q(estado='devuelto')),
            retrasados=Count('id', filter=Q(estado='retrasado'))
        )
        
        context.update(stats)
        
        context['total_reservas'] = Reserva.objects.filter(
            usuario=perfil
        ).count()
        
        context['reservas_pendientes'] = Reserva.objects.filter(
            usuario=perfil,
            estado='pendiente'
        ).count()
        
        return context

class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = PerfilUsuarioForm
    template_name = "usuarios/editar_perfil.html"
    success_url = reverse_lazy("usuarios:perfil")

    def get_object(self):
        return self.request.user

class CambiarContrasenaView(LoginRequiredMixin, PasswordChangeView):
    template_name = "usuarios/cambiar_contrasena.html"
    success_url = reverse_lazy("usuarios:perfil")