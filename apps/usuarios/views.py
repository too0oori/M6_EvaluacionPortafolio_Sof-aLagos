from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistroForm, PerfilForm

class LoginUsuarioView(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True

class RegistroUsuarioView(CreateView, View):
    model = User
    template_name = "auth/registro.html"
    form_class = RegistroForm
    success_url = reverse_lazy("usuarios:login")  # redirige al login tras registrarse

class LogoutUsuarioView(LogoutView):
    template_name = "auth/logout.html"

class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = "usuarios/perfil.html"


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