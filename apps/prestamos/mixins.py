#mixins 
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginRequiredMixin(LoginRequiredMixin):
    login_url = '/auth/login/'
    redirect_field_name = 'next'