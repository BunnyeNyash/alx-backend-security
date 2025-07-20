from celery import shared_task
from django.utils import timezone
from ip_tracking.models import RequestLog, SuspiciousIP
from datetime import timedelta
from django.db import models

@shared_task
def detect_anomalies():
    time_threshold = timezone.now() - timedelta(hours=1)
    sensitive_paths = ['/admin', '/login']
    
    ip_requests = RequestLog.objects.filter(
        timestamp__gte=time_threshold
    ).values('ip_address').annotate(
        request_count=models.Count('id')
    ).filter(request_count__gt=100)
    
    for ip_data in ip_requests:
        ip = ip_data['ip_address']
        count = ip_data['request_count']
        if not SuspiciousIP.objects.filter(ip_address=ip, reason__contains='High request rate').exists():
            SuspiciousIP.objects.create(
                ip_address=ip,
                reason=f"High request rate: {count} requests in the last hour"
            )
    
    sensitive_requests = RequestLog.objects.filter(
        timestamp__gte=time_threshold,
        path__in=sensitive_paths
    ).values('ip_address').distinct()
    
    for ip_data in sensitive_requests:
        ip = ip_data['ip_address']
        if not SuspiciousIP.objects.filter(ip_address=ip, reason__contains='Sensitive path access').exists():
            SuspiciousIP.objects.create(
                ip_address=ip,
                reason="Accessed sensitive path (e.g., /admin or /login)"
            )
