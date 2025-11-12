from django.shortcuts import render

def dashboard_reportes(request):
    return render(request, 'templates/reportes/dashboard.html')

def libros_mas_prestados(self):
    # Lógica para obtener los libros más prestados
    pass

def usuarios_mas_activos(self):
    # Lógica para obtener los usuarios más activos
    pass

def prestamos_atrasados(self):
    # Lógica para obtener los préstamos atrasados
    pass

def estadisticas_generales(self):
    # Lógica para obtener estadísticas generales
    pass