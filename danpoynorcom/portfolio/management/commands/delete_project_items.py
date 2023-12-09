from django.core.management.base import BaseCommand
from portfolio.models import ProjectItem


class Command(BaseCommand):
    help = 'Delete all project items'

    def handle(self, *args, **options):
        # Delete all ProjectItem instances
        ProjectItem.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all project items'))
