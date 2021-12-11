from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """ This middleware checks if the user is authenticated. """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.available_views = ['user_login', 'user_register']
        
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    
    def process_view(self, request, view_func, *args, **kwargs):
        if self._view_is_valid_for_check(view_func.__name__):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('User:login')}?loginRequired=1")
    
    
    def _view_is_valid_for_check(self, view_name):
        return not view_name in self.available_views