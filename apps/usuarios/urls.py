from django.urls import path
from . import views
from .views import PerfilUsuarioView, LoginUsuarioView, LogoutUsuarioView, RegistroUsuarioView, EditarPerfilView, CambiarContrasenaView

app_name = 'usuarios'

urlpatterns = [
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('editar_perfil/', EditarPerfilView.as_view(), name='editar_perfil'),
    path('cambiar_contrasena/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
]