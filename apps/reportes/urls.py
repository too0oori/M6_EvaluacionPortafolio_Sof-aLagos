from django.urls import path
from . import views
from .views import DashboardReportesView

app_name = 'reportes'

urlpatterns = [
    path('dashboard/', DashboardReportesView.as_view(), name='dashboard'),
]