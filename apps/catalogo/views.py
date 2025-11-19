from django.shortcuts import render
from django.views import View
from django.db.models import Q
from .models import Libro, Autor, Categoria

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
        libro = Libro.objects.get(id=libro_id)
        return render(request, self.template_name, {'libro': libro})

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