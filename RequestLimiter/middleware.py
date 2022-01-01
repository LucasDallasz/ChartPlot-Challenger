from django.http import JsonResponse

from .utils import date_time_now

class RequestLimiterMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.available_views = ['user_register', 'user_login']
        self.error_message = 'Detectamos um tráfego incomum de dados. Aguarde para realizar uma nova requisição.'
        
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    
    def process_view(self, request, view, *args, **kwargs):
        if request.method == 'POST' and self._view_is_valid(view.__name__):
            user = request.user
            user_last_request = user.get_last_post_request()
            now_request = date_time_now()
            punishment_seconds = user.get_punishment_seconds()
            if not self._request_is_valid(user_last_request, now_request, punishment_seconds):
                user.set_last_post_request(now_request.__str__())
                user.increment_punishment_seconds()
                user.increment_sequence_invalid_requests()
                return JsonResponse({'status': 403, 'message': self.error_message, 'punishment_seconds': punishment_seconds})
            user.set_last_post_request(now_request.__str__())
            self._clean_user(user)
    
    
    def _request_is_valid(self, last, now, punishment_seconds) -> bool:
        return (now - last).total_seconds() > punishment_seconds
       
       
    def _view_is_valid(self, view_name) -> bool:
        return view_name not in self.available_views
    
    
    def _clean_user(self, user):
        punishment_seconds_default, zero_sequences = 2, 0
        user.punishment_seconds = punishment_seconds_default
        user.sequence_invalid_requests = zero_sequences
        user.save()