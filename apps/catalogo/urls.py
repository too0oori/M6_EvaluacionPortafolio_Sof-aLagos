from django.urls import path
from . import views
from .views import HomePageView, ListaLibrosView, DetalleLibroView

app_name = 'catalogo'

urlpatterns = [

    path('', HomePageView.as_view(), name='home'),
    path('libros/', ListaLibrosView.as_view(), name='lista_libros'),
    path('libros/<int:libro_id>/', DetalleLibroView.as_view(), name='detalle_libro'),
]