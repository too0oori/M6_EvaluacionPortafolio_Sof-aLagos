#mixins 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class LoginRequiredMixin(LoginRequiredMixin):
    login_url = '/auth/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
class AdminRequiredMixin(PermissionRequiredMixin):
    permission_required = 'prestamos.delete_prestamo'
    login_url = '/auth/login/'
    redirect_field_name = 'next'