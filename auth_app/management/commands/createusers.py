from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from auth_app.models import Users, MerchantInformation
from client_app.models import Tenant


class Command(BaseCommand):
    help = 'Create dummy superadmin, merchant admin merchant staff'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        with transaction.atomic():
            superadmin = Users.objects.create_superuser(
                name="saifullah",
                phone_number="+8801752495467",
                password="123456"
            )
            # merchant owner create
            mer_owner = Users.objects.create_merchant_owner(
                name="saifullah",
                phone_number="+8801752495466",
                password="123456",
            )
            tenower = Tenant.objects.create(
                url="saifullah",
            )
            mer_owner.merchant_accepted_by_superadmin = superadmin
            mer_owner.save()
            MerchantInformation.objects.create(
                user=mer_owner,
                merchant_domain=tenower,
                company_name="Saif company"
            )
            # create merchant admin
            mer_admin = Users.objects.create_merchant_admin(
                name="saifullah",
                phone_number="+8801752495464",
                password="123456",
            )
            MerchantInformation.objects.create(
                user=mer_admin,
                merchant_domain=tenower,
                merchant_parent_who_created=mer_owner,
                company_name="Saif company"
            )
            # create merchant staff
            mer_staff = Users.objects.create_merchant_staff(
                name="saifullah",
                phone_number="+8801752495462",
                password="123456",
            )
            MerchantInformation.objects.create(
                user=mer_staff,
                merchant_domain=tenower,
                merchant_parent_who_created=mer_admin,
                company_name="Saif company"
            )
            # create user
            user = Users.objects.create_user(
                name="saifullah",
                phone_number="+8801752495445",
                password="123456",
            )
