from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = 'Add an IP address to the blacklist'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='IP address to block')
        parser.add_argument('--reason', type=str, default='', help='Reason for blocking')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        reason = options['reason']
        
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            self.stdout.write(self.style.WARNING(f'IP {ip_address} is already blacklisted.'))
        else:
            BlockedIP.objects.create(ip_address=ip_address, reason=reason)
            self.stdout.write(self.style.SUCCESS(f'Successfully blacklisted IP {ip_address}'))
