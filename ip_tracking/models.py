from django.db import models

# Create your models here.
class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"

    class Meta:
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['timestamp']),
        ]

class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True)

    def __str__(self):
        return self.ip_address
