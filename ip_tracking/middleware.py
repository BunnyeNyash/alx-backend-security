from django.conf import settings
from ip_tracking.models import RequestLog, BlockedIP
from django_ipware import get_client_ip
from django.http import HttpResponseForbidden
from django.core.cache import cache
from ip2geotools.databases.commercial import IpStack
import os

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geo_api = IpStack(os.getenv('IP2GEOTOOLS_API_KEY'))

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

            cache_key = f"geo_{client_ip}"
            geo_data = cache.get(cache_key)
            if not geo_data:
                try:
                    response = self.geo_api.get_location(client_ip)
                    geo_data = {
                        'country': response.country_name or '',
                        'city': response.city or ''
                    }
                    cache.set(cache_key, geo_data, timeout=24*60*60)  # Cache for 24 hours
                except Exception as e:
                    geo_data = {'country': '', 'city': ''}
                    print(f"Geolocation error: {e}")
                    
            RequestLog.objects.create(
                ip_address=log_ip,
                path=request.path,
                country=geo_data['country'],
                city=geo_data['city']
            )
        
        response = self.get_response(request)
        return response
