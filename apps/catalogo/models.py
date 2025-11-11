from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nombre
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.nombre
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    ano_publicacion = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()
    portada = models.ImageField(upload_to='portadas')
    copias_totales = models.PositiveIntegerField()
    copias_disponibles = models.PositiveIntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titulo
    
