from urllib import request
from django.shortcuts import render
from django.views import View

class HomePageView(View):
    template_name = 'catalogo/home.html'

    def get(self, request):
        return render(request, self.template_name)

class ListaLibrosView(View):
    template_name = 'catalogo/lista_libros.html'

    def get(self, request):
        return render(request, self.template_name)

class DetalleLibroView(View):
    template_name = 'catalogo/detalle_libro.html'

    def get(self, request, libro_id):
        return render(request, self.template_name, {'libro_id': libro_id})

class BuscarLibrosView(View):
    template_name = 'catalogo/buscar_libros.html'

    def get(self, request):
        return render(request, self.template_name)

class FiltrarPorCategoriaView(View):
    template_name = 'catalogo/filtrar.html'

    def get(self, request, categoria):
        return render(request, self.template_name, {'categoria': categoria})

class ListaAutoresView(View):
    template_name = 'catalogo/lista_autores.html'

    def get(self, request):
        return render(request, self.template_name)

class DetalleAutorView(View):
    template_name = 'catalogo/detalle_autor.html'

    def get(self, request, autor_id):
        return render(request, self.template_name, {'autor_id': autor_id})