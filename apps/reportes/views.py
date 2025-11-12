from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.db.models import Count
from apps.prestamos.models import Prestamo
from apps.catalogo.models import Libro
from django.utils import timezone
from django.contrib.auth.models import User

class DashboardReportesView(TemplateView):
    template_name = 'reportes/dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Bibliotecarios').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = super().get_context_data(**kwargs)

        context['libros_mas_prestados'] = self.get_libros_mas_prestados()
        context['usuarios_mas_activos'] = self.get_usuarios_mas_activos()
        context['prestamos_atrasados'] = self.get_prestamos_atrasados()
        context['estadisticas_generales'] = self.get_estadisticas_generales()

        return context
    
    
    def get_libros_mas_prestados(self):
        return Prestamo.objects.values('libro__titulo').annotate(total=Count('libro')).order_by('-total')[:5]
    
    def get_usuarios_mas_activos(self):
        return User.objects.annotate(total_prestamos=Count('prestamo')).order_by('-total_prestamos')[:5]
    
    def get_prestamos_atrasados(self):
        return Prestamo.objects.filter(fecha_devolucion__isnull=True, fecha_limite__lt=timezone.now())
    
    def get_estadisticas_generales(self):
        prestamos_totales = Prestamo.objects.count()
        libros_totales = Libro.objects.count()
        usuarios_totales = User.objects.count()
        prestamos_atrasados = Prestamo.objects.filter(fecha_devolucion__isnull=True).count()
        return {
            'prestamos_totales': prestamos_totales,
            'libros_totales': libros_totales,
            'usuarios_totales': usuarios_totales,
            'prestamos_atrasados': prestamos_atrasados,
        }