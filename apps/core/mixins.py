from django.contrib.auth.mixins import LoginRequiredMixin as DjangoLoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class LoginRequiredMixin(DjangoLoginRequiredMixin):
    login_url = '/usuarios/login/'
    redirect_field_name = 'next'

class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class BibliotecarioRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Permite acceso a bibliotecarios y administradores"""
    
    def test_func(self):
        user = self.request.user
        return (
            user.groups.filter(name='Bibliotecarios').exists() or 
            user.is_staff or 
            user.is_superuser
        )
    
    def handle_no_permission(self):
        messages.error(
            self.request, 
            'No tienes permisos de bibliotecario para acceder a esta sección.'
        )
        return redirect('catalogo:home')