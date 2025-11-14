
from django.contrib.auth.models import User, Group, Permission
from apps.catalogo.models import Categoria, Autor, Libro
from apps.prestamos.models import Prestamo, Reserva
from apps.usuarios.models import PerfilUsuario
from django.utils import timezone
from datetime import timedelta


# ============================================
# 1. CREAR GRUPOS Y PERMISOS
# ============================================

bibliotecarios, _ = Group.objects.get_or_create(name='Bibliotecarios')
usuarios_regulares, _ = Group.objects.get_or_create(name='Usuarios Regulares')

permisos_bibliotecario = Permission.objects.filter(
    content_type__app_label__in=['catalogo', 'prestamos', 'usuarios'])
bibliotecarios.permissions.set(permisos_bibliotecario)
print("Grupos creados")

# ============================================
# 2. CREAR USUARIOS
# ============================================

# Bibliotecarios
bibliotecarios_data = [
    {'username': 'harito.haru', 'first_name': 'Harito', 'last_name': 'Haru', 
     'email': 'harito@biblioteca.com', 'telefono': '+56912345678', 
     'direccion': 'Av. Providencia 123, Santiago'},
    {'username': 'luna.luni', 'first_name': 'Luna', 'last_name': 'Luni', 
     'email': 'luna@biblioteca.com', 'telefono': '+56923456789', 
     'direccion': 'Calle Huerfanos 456, Santiago'},
]

print("  Creando bibliotecarios...")
for data in bibliotecarios_data:
    try:
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='biblio123',
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            user.groups.add(bibliotecarios)
            
            # Crear perfil
            perfil, _ = PerfilUsuario.objects.get_or_create(usuario=user)
            perfil.telefono = data['telefono']
            perfil.direccion = data['direccion']
            perfil.save()
            
            print(f" {data['username']}")
        else:
            print(f"{data['username']}")
    except Exception as e:
        print(f"    [ERROR] {data['username']}: {e}")

# Usuarios regulares
usuarios_data = [
    {'username': 'michi.michi', 'first_name': 'Michi', 'last_name': 'Micho', 
     'email': 'michi@gatitos.com', 'telefono': '+56934567890', 
     'direccion': 'Calle Moneda 789, Santiago'},
    {'username': 'luna.lunatica', 'first_name': 'Luna', 'last_name': 'Lunatica', 
     'email': 'luna@gatitos.com', 'telefono': '+56945678901', 
     'direccion': 'Av. Libertador 234, Santiago'},
    {'username': 'koko.kokito', 'first_name': 'Koko', 'last_name': 'Kokito', 
     'email': 'koko@perritos.com', 'telefono': '+56956789012', 
     'direccion': 'Calle Ahumada 567, Santiago'},
    {'username': 'chico.tyson', 'first_name': 'Chico', 'last_name': 'Tyson', 
     'email': 'tyson@perritos.com', 'telefono': '+56967890123', 
     'direccion': 'Av. Apoquindo 890, Las Condes'},
    {'username': 'mizuki.zuka', 'first_name': 'Mizuki', 'last_name': 'Zuka', 
     'email': 'mizuki@perritos.com', 'telefono': '+56978901234', 
     'direccion': 'Calle Bandera 345, Santiago'},
    {'username': 'mely.antonia', 'first_name': 'Melisa', 'last_name': 'Antonia', 
     'email': 'mely@perritos.com', 'telefono': '+56989012345', 
     'direccion': 'Av. Providencia 456, Providencia'},
    {'username': 'crazy.aiko', 'first_name': 'Aiko', 'last_name': 'Aiko', 
     'email': 'aiko@perritos.com', 'telefono': '+56990123456', 
     'direccion': 'Calle Estado 123, Santiago'},
]

print("  Creando usuarios regulares...")
for data in usuarios_data:
    try:
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='usuario123',
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            user.groups.add(usuarios_regulares)
            
            # Crear perfil
            perfil, _ = PerfilUsuario.objects.get_or_create(usuario=user)
            perfil.telefono = data['telefono']
            perfil.direccion = data['direccion']
            perfil.save()
            
            print(f"{data['username']}")
        else:
            print(f" {data['username']}")
    except Exception as e:
        print(f"    [ERROR] {data['username']}: {e}")

# ============================================
# 3. CREAR CATEGORIAS
# ============================================

categorias_data = [
    {'nombre': 'Ficcion', 'descripcion': 'Novelas y cuentos de ficcion'},
    {'nombre': 'No Ficcion', 'descripcion': 'Libros basados en hechos reales'},
    {'nombre': 'Filosofia', 'descripcion': 'Textos filosoficos y ensayos'},
]

for cat_data in categorias_data:
    cat, created = Categoria.objects.get_or_create(
        nombre=cat_data['nombre'],
        defaults={'descripcion': cat_data['descripcion']}
    )
    if created:
        print(f" {cat.nombre}")
    else:
        print(f"{cat.nombre}")

# ============================================
# 4. CREAR AUTORES 
# ============================================

autores_data = [
    {'nombre': 'Clarice Lispector', 'pais': 'Brasil', 'fecha_nacimiento': '1920-12-10', 
     'biografia': 'Escritora brasilena'},
    {'nombre': 'Sylvia Plath', 'pais': 'Estados Unidos', 'fecha_nacimiento': '1932-10-27', 
     'biografia': 'Poeta estadounidense'},
    {'nombre': 'Nelly Richard', 'pais': 'Chile', 'fecha_nacimiento': '1948-01-01', 
     'biografia': 'Teorica cultural chilena'},
    {'nombre': 'Diamela Eltit', 'pais': 'Chile', 'fecha_nacimiento': '1949-08-24', 
     'biografia': 'Escritora chilena experimental'},
    {'nombre': 'Gabriela Mistral', 'pais': 'Chile', 'fecha_nacimiento': '1889-04-07', 
     'biografia': 'Poeta chilena Nobel'},
    {'nombre': 'Virginia Woolf', 'pais': 'Reino Unido', 'fecha_nacimiento': '1882-01-25', 
     'biografia': 'Escritora modernista'},
    {'nombre': 'Simone de Beauvoir', 'pais': 'Francia', 'fecha_nacimiento': '1908-01-09', 
     'biografia': 'Filosofa y feminista'},
    {'nombre': 'Alejandra Pizarnik', 'pais': 'Argentina', 'fecha_nacimiento': '1936-04-29', 
     'biografia': 'Poeta argentina'},
    {'nombre': 'Isabel Allende', 'pais': 'Chile', 'fecha_nacimiento': '1942-08-02', 
     'biografia': 'Escritora chilena'},
    {'nombre': 'Marguerite Duras', 'pais': 'Francia', 'fecha_nacimiento': '1914-04-04', 
     'biografia': 'Escritora francesa'},
    {'nombre': 'Marguerite Yourcenar', 'pais': 'Belgica', 'fecha_nacimiento': '1903-06-08', 
     'biografia': 'Primera mujer en Academia Francesa'},
    {'nombre': 'Toni Morrison', 'pais': 'Estados Unidos', 'fecha_nacimiento': '1931-02-18', 
     'biografia': 'Escritora afroamericana Nobel'},
    {'nombre': 'Annie Ernaux', 'pais': 'Francia', 'fecha_nacimiento': '1940-09-01', 
     'biografia': 'Escritora francesa contemporanea'},
]

for autor_data in autores_data:
    autor, created = Autor.objects.get_or_create(
        nombre=autor_data['nombre'],
        defaults={
            'pais': autor_data['pais'],
            'fecha_nacimiento': autor_data['fecha_nacimiento'],
            'biografia': autor_data['biografia']
        }
    )
    if created:
        print(f"{autor.nombre}")
    else:
        print(f"{autor.nombre}")

# ============================================
# 5. CREAR LIBROS
# ============================================

libros_data = [
    # CLARICE LISPECTOR
    {'titulo': 'La hora de la estrella', 'autor': 'Clarice Lispector', 'isbn': '9788416120796', 
     'editorial': 'Siruela', 'ano': 1977, 'categoria': 'Ficcion', 
     'descripcion': 'Ultima novela de Lispector', 'copias': 3},
    {'titulo': 'La pasion segun G.H.', 'autor': 'Clarice Lispector', 'isbn': '9788478445523', 
     'editorial': 'Siruela', 'ano': 1964, 'categoria': 'Ficcion', 
     'descripcion': 'Obra sobre identidad', 'copias': 3},
    {'titulo': 'Agua viva', 'autor': 'Clarice Lispector', 'isbn': '9788478444519', 
     'editorial': 'Siruela', 'ano': 1973, 'categoria': 'Ficcion', 
     'descripcion': 'Prosa poetica', 'copias': 2},
    
    # SYLVIA PLATH
    {'titulo': 'La campana de cristal', 'autor': 'Sylvia Plath', 'isbn': '9788439736349', 
     'editorial': 'Edhasa', 'ano': 1963, 'categoria': 'Ficcion', 
     'descripcion': 'Novela autobiografica', 'copias': 4},
    {'titulo': 'Ariel', 'autor': 'Sylvia Plath', 'isbn': '9788498410686', 
     'editorial': 'Bartleby', 'ano': 1965, 'categoria': 'Ficcion', 
     'descripcion': 'Poemas postumos', 'copias': 3},
    
    # NELLY RICHARD
    {'titulo': 'Fracturas de la memoria', 'autor': 'Nelly Richard', 'isbn': '9789562890793', 
     'editorial': 'Siglo XXI', 'ano': 2007, 'categoria': 'Filosofia', 
     'descripcion': 'Ensayos sobre arte y politica', 'copias': 2},
    
    # DIAMELA ELTIT
    {'titulo': 'Lumperica', 'autor': 'Diamela Eltit', 'isbn': '9789568415204', 
     'editorial': 'Seix Barral', 'ano': 1983, 'categoria': 'Ficcion', 
     'descripcion': 'Novela experimental', 'copias': 2},
    
    # GABRIELA MISTRAL
    {'titulo': 'Desolacion', 'autor': 'Gabriela Mistral', 'isbn': '9789561603738', 
     'editorial': 'Andres Bello', 'ano': 1922, 'categoria': 'Ficcion', 
     'descripcion': 'Primera obra poetica', 'copias': 3},
    
    # VIRGINIA WOOLF
    {'titulo': 'La senora Dalloway', 'autor': 'Virginia Woolf', 'isbn': '9788426418210', 
     'editorial': 'Lumen', 'ano': 1925, 'categoria': 'Ficcion', 
     'descripcion': 'Un dia en Londres', 'copias': 4},
    {'titulo': 'Al faro', 'autor': 'Virginia Woolf', 'isbn': '9788426418227', 
     'editorial': 'Lumen', 'ano': 1927, 'categoria': 'Ficcion', 
     'descripcion': 'Obra modernista', 'copias': 3},
    {'titulo': 'Una habitacion propia', 'autor': 'Virginia Woolf', 'isbn': '9788432248528', 
     'editorial': 'Seix Barral', 'ano': 1929, 'categoria': 'Filosofia', 
     'descripcion': 'Ensayo feminista', 'copias': 4},
    
    # SIMONE DE BEAUVOIR
    {'titulo': 'El segundo sexo', 'autor': 'Simone de Beauvoir', 'isbn': '9788437629841', 
     'editorial': 'Catedra', 'ano': 1949, 'categoria': 'Filosofia', 
     'descripcion': 'Obra feminista fundamental', 'copias': 4},
    {'titulo': 'Los mandarines', 'autor': 'Simone de Beauvoir', 'isbn': '9788435018081', 
     'editorial': 'Edhasa', 'ano': 1954, 'categoria': 'Ficcion', 
     'descripcion': 'Intelectuales parisinos', 'copias': 2},
    
    # ALEJANDRA PIZARNIK
    {'titulo': 'Arbol de Diana', 'autor': 'Alejandra Pizarnik', 'isbn': '9789500739153', 
     'editorial': 'Losada', 'ano': 1962, 'categoria': 'Ficcion', 
     'descripcion': 'Poemario', 'copias': 3},
    
    # ISABEL ALLENDE
    {'titulo': 'La casa de los espiritus', 'autor': 'Isabel Allende', 'isbn': '9788401242359', 
     'editorial': 'Plaza & Janes', 'ano': 1982, 'categoria': 'Ficcion', 
     'descripcion': 'Saga familiar chilena', 'copias': 4},
    {'titulo': 'Paula', 'autor': 'Isabel Allende', 'isbn': '9780060927219', 
     'editorial': 'HarperCollins', 'ano': 1994, 'categoria': 'No Ficcion', 
     'descripcion': 'Memorias', 'copias': 3},
    
    # MARGUERITE DURAS
    {'titulo': 'El amante', 'autor': 'Marguerite Duras', 'isbn': '9788483831441', 
     'editorial': 'Tusquets', 'ano': 1984, 'categoria': 'Ficcion', 
     'descripcion': 'Novela autobiografica', 'copias': 3},
    
    # MARGUERITE YOURCENAR
    {'titulo': 'Memorias de Adriano', 'autor': 'Marguerite Yourcenar', 'isbn': '9788435018111', 
     'editorial': 'Edhasa', 'ano': 1951, 'categoria': 'Ficcion', 
     'descripcion': 'Novela historica', 'copias': 3},
    
    # TONI MORRISON
    {'titulo': 'Beloved', 'autor': 'Toni Morrison', 'isbn': '9780307264886', 
     'editorial': 'Vintage', 'ano': 1987, 'categoria': 'Ficcion', 
     'descripcion': 'Novela sobre esclavitud', 'copias': 4},
    {'titulo': 'Ojos azules', 'autor': 'Toni Morrison', 'isbn': '9780307278449', 
     'editorial': 'Vintage', 'ano': 1970, 'categoria': 'Ficcion', 
     'descripcion': 'Sobre racismo', 'copias': 3},

    # ANNIE ERNAUX
    {'titulo': 'Los años', 'autor': 'Annie Ernaux', 'isbn': '9788490666449',
     'editorial': 'Cabaret Voltaire', 'ano': 2008, 'categoria': 'No Ficcion',
     'descripcion': 'Memoria colectiva y personal. Relato de vida, tiempo e identidad femenina.', 'copias': 4},

    {'titulo': 'El acontecimiento', 'autor': 'Annie Ernaux', 'isbn': '9788433979247',
     'editorial': 'Tusquets', 'ano': 2000, 'categoria': 'No Ficcion',
     'descripcion': 'Testimonio íntimo sobre el aborto clandestino y la autonomía del cuerpo.', 'copias': 3},

]

for libro_data in libros_data:
    try:
        autor = Autor.objects.get(nombre=libro_data['autor'])
        categoria = Categoria.objects.get(nombre=libro_data['categoria'])
        
        libro, created = Libro.objects.get_or_create(
            isbn=libro_data['isbn'],
            defaults={
                'titulo': libro_data['titulo'],
                'autor': autor,
                'editorial': libro_data['editorial'],
                'ano_publicacion': libro_data['ano'],
                'categoria': categoria,
                'descripcion': libro_data['descripcion'],
                'copias_totales': libro_data['copias'],
                'copias_disponibles': libro_data['copias']
            }
        )
        if created:
            print(f"  {libro.titulo}")
        else:
            print(f"{libro.titulo}")
    except Exception as e:
        print(f"  [ERROR] {libro_data['titulo']}: {e}")

# ============================================
# 6. CREAR PRESTAMOS
# ============================================

prestamos_activos = [
    {'usuario': 'michi.michi', 'libro': 'La hora de la estrella', 'dias': 5},
    {'usuario': 'luna.lunatica', 'libro': 'La campana de cristal', 'dias': 10},
    {'usuario': 'koko.kokito', 'libro': 'El segundo sexo', 'dias': 3},
]

for prestamo_data in prestamos_activos:
    try:
        usuario = PerfilUsuario.objects.get(usuario__username=prestamo_data['usuario'])
        libro = Libro.objects.get(titulo=prestamo_data['libro'])

        if not Prestamo.objects.filter(usuario=usuario, libro=libro, estado='activo').exists():
            fecha_prestamo = timezone.now() - timedelta(days=prestamo_data['dias'])
            fecha_devolucion = fecha_prestamo + timedelta(days=14)

            Prestamo.objects.create(
                usuario=usuario,
                libro=libro,
                fecha_prestamo=fecha_prestamo,
                fecha_devolucion=fecha_devolucion.date(),
                estado='activo'
            )

            libro.copias_disponibles = max(libro.copias_disponibles - 1, 0)
            libro.save()

            print(f"{libro.titulo} -> {usuario.usuario.username}")
        else:
            print(f"  Prestamo ya existe")
    except Exception as e:
        print(f"  [ERROR] {e}")

# ============================================
# 7. CREAR RESERVAS
# ============================================

reservas_data = [
    {'usuario': 'crazy.aiko', 'libro': 'Una habitacion propia'},
    {'usuario': 'mely.antonia', 'libro': 'Lumperica'},
]

for reserva_data in reservas_data:
    try:
        usuario = PerfilUsuario.objects.get(usuario__username=reserva_data['usuario'])
        libro = Libro.objects.get(titulo=reserva_data['libro'])

        reserva, created = Reserva.objects.get_or_create(
            usuario=usuario,
            libro=libro,
            defaults={'estado': 'pendiente'}
        )
        if created:
            print(f"{libro.titulo} -> {usuario.usuario.username}")
        else:
            print(f"  Reserva ya existe")
    except Exception as e:
        print(f"  [ERROR] {e}")

print("\nPOBLACION DE BASE DE DATOS COMPLETADA")


# PARA CARGAR PORTADAS DE LIBROS DESDE URLS EN BASE A ISBN


from apps.catalogo.models import Libro

for libro in Libro.objects.all():
    if libro.isbn:  # solo si tiene ISBN
        nueva_portada = f"https://covers.openlibrary.org/b/isbn/{libro.isbn}-L.jpg"
        libro.portada = nueva_portada
        libro.save()
        print(f"✓ Portada actualizada: {libro.titulo}")
    else:
        print(f"Sin ISBN, no se puede actualizar: {libro.titulo}")