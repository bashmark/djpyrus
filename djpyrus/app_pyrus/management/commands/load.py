from django.contrib.auth.models import User
from django.core.management import BaseCommand

from ...functions.load_kk_in_db import load_kk_in_db
from ...models import RevisionModel
from ...tasks import load
from ...config import ADMIN_PASS


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_kk_in_db()
