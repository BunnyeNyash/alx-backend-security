from django.conf import settings
from ip_tracking.models import RequestLog
from django_ipware import get_client_ip

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip, is_routable = get_client_ip(request)
        if client_ip:
            if '.' in client_ip:
                client_ip = '.'.join(client_ip.split('.')[:-1] + ['0'])
            else:
                client_ip = ':'.join(client_ip.split(':')[:-4] + ['0' * 4])
            
            RequestLog.objects.create(
                ip_address=client_ip,
                path=request.path
            )
        
        response = self.get_response(request)
        return response
