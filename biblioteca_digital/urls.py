from django.conf import settings
from django.contrib import admin
from django.urls import include, path 
from django.views.generic import TemplateView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('catalogo/', include('apps.catalogo.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('prestamos/', include('apps.prestamos.urls')),
    path('reportes/', include('apps.reportes.urls')),
]

# Configuracion para servir archivos multimedia en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)