from django.core.management.base import BaseCommand
from main.bot import run_bot


class Command(BaseCommand):
    help = 'Run bot'

    def handle(self, *args, **options):
        run_bot()