from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Libro, Autor, Categoria
from django.contrib import messages
from django.http import Http404
from django.views import View
class HomePageView(View):
    template_name = 'catalogo/home.html'

    def get(self, request):
        return render(request, self.template_name)

class ListaLibrosView(View):
    template_name = 'catalogo/lista_libros.html'

    def get(self, request):
        q = request.GET.get('q', '').strip()
        categoria = request.GET.get('categoria', '').strip()
        autor = request.GET.get('autor', '').strip()

        libros = Libro.objects.all()

        if q:
            libros = libros.filter(
                Q(titulo__icontains=q) | Q(autor__nombre__icontains=q) | Q(isbn__icontains=q)
            )

        if categoria:
            libros = libros.filter(categoria__nombre=categoria)

        if autor:
            libros = libros.filter(autor__nombre=autor)


        from django.core.paginator import Paginator #para paginación
        
        paginator = Paginator(libros, 12)  # 12 libros por página
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'libros': page_obj,
            'q': q,
            'categorias': Categoria.objects.all(),
            'autores': Autor.objects.all(),
            'categoria_activa': categoria,
            'autor_activo': autor,
            'total_resultados': libros.count()
        }

        return render(request, self.template_name, context)

class DetalleLibroView(View):
    template_name = 'catalogo/detalle_libro.html'

    def get(self, request, libro_id):
        try:
            libro = get_object_or_404(Libro, id=libro_id)
            return render(request, self.template_name, {'libro': libro})
        except Http404:
            messages.error(request, "Libro no encontrado")
            return redirect('catalogo:lista_libros')