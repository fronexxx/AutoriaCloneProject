import time

from django.core.management.base import BaseCommand
from django.db import OperationalError, connections


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database')

        con_db = None

        while not con_db:
            try:
                con_db = connections['default']
                con_db.ensure_connection()

            except OperationalError:
                self.stdout.write('Database unavailable, wait 3 seconds...')
                time.sleep(3)

        self.stdout.write(self.style.SUCCESS('Database available!'))
