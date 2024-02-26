import logging

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from ...models import RevisionModel
from ...tasks import load
from ...config import ADMIN_PASS


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not RevisionModel.objects.filter(id=1).exists():
            RevisionModel.objects.create(revision=1)
            load.delay()
        if User.objects.count() == 0:
            username = 'admin'
            email = 'bashmark@mail.ru'
            password = ADMIN_PASS
            logging.info('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            logging.info('Admin accounts can only be initialized if no Accounts exist')