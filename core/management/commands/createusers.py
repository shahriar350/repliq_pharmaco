from django.core.management import BaseCommand

from accountio.models import Merchant


class Command(BaseCommand):
    help = 'Create dummy information...'

    def handle(self, *args, **options):
        Merchant.objects.create_merchant_admin("Saifullah Admin", "+8801521475691", "123456")
        Merchant.objects.create_merchant_owner("Saifullah Owner", "+8801521475690", "123456")
        Merchant.objects.create_merchant_staff("Saifullah Staff", "+8801521475692", "123456")
