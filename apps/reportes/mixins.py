from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin 

class ReporteRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'reportes.view_reporte'
    login_url = '/auth/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
