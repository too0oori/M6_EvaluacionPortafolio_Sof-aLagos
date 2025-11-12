from django.urls import path
from . import views
from .views import HomePageView, ListaLibrosView, DetalleLibroView, ListaAutoresView, DetalleAutorView, FiltrarPorCategoriaView, BuscarLibrosView

app_name = 'catalogo'

urlpatterns = [

    path('', HomePageView.as_view(), name='home'),
    path('libros/', ListaLibrosView.as_view(), name='lista_libros'),
    path('libros/<int:libro_id>/', DetalleLibroView.as_view(), name='detalle_libro'),
    path('autores/', ListaAutoresView.as_view(), name='autores'),
    path('autores/<int:autor_id>/', DetalleAutorView.as_view(), name='detalle_autor'),
    path('filtrar/<str:categoria>/', FiltrarPorCategoriaView.as_view(), name='filtrar_por_categoria'),
    path('buscar_libros/', BuscarLibrosView.as_view(), name='buscar_libros'),
]