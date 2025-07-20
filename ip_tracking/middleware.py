from django.conf import settings
from ip_tracking.models import RequestLog, BlockedIP
from django_ipware import get_client_ip
from django.http import HttpResponseForbidden

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip, is_routable = get_client_ip(request)
        if client_ip:
            if BlockedIP.objects.filter(ip_address=client_ip).exists():
                return HttpResponseForbidden("Access denied: Your IP is blacklisted.")
            
            log_ip = client_ip
            if '.' in log_ip:
                log_ip = '.'.join(log_ip.split('.')[:-1] + ['0'])
            else:
                log_ip = ':'.join(log_ip.split(':')[:-4] + ['0' * 4])
            
            RequestLog.objects.create(
                ip_address=log_ip,
                path=request.path
            )
        
        response = self.get_response(request)
        return response
