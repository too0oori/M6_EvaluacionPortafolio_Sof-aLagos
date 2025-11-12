from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.catalogo.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('prestamos/', include('apps.prestamos.urls')),
    path('reportes/', include('apps.reportes.urls')),
]