from django.shortcuts import render

def home(request):
    return render(request, 'templates/catalogo/home.html')

def lista_libros(request):
    return render(request, 'templates/catalogo/lista_libros.html')

def detalle_libro(request, libro_id):
    return render(request, 'templates/catalogo/detalle_libro.html', {'libro_id': libro_id})

def buscar_libros(request):
    return render(request, 'templates/catalogo/buscar_libros.html')

def filtrar_por_categoria(request, categoria):
    return render(request, 'templates/catalogo/filtrar.html', {'categoria': categoria})

def lista_autores(request):
    return render(request, 'templates/catalogo/lista_autores.html')

def detalle_autor(request, autor_id):
    return render(request, 'templates/catalogo/detalle_autor.html', {'autor_id': autor_id})