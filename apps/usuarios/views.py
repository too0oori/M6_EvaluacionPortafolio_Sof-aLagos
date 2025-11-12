from django.shortcuts import render

def login_view(request):
    return render(request, 'templates/auth/login.html')

def registro_view(request):
    return render(request, 'templates/auth/registro.html')

def logout_view(LoginRequiredMixin, request):
    return render(request, 'templates/auth/logout.html')

def perfil_usuario(LoginRequiredMixin, request):
    return render(request, 'templates/usuarios/perfil.html')

def editar_perfil(LoginRequiredMixin, request):
    return render(request, 'templates/usuarios/editar_perfil.html')

def cambiar_contrasena(LoginRequiredMixin, request):
    return render(request, 'templates/usuarios/cambiar_contrasena.html')