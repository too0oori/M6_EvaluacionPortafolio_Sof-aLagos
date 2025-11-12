from django.contrib import admin
from django.urls import include, path 
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html')),
    path('catalogo/', include('apps.catalogo.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('prestamos/', include('apps.prestamos.urls')),
    path('reportes/', include('apps.reportes.urls')),
]