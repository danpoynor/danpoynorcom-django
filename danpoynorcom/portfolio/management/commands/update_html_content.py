from django.core.management.base import BaseCommand
from portfolio.models import ProjectItem

class Command(BaseCommand):
    help = 'Updates html_content field of ProjectItem instances'

    def handle(self, *args, **options):
        # Get all ProjectItem instances
        project_items = ProjectItem.objects.all()

        # Iterate over the ProjectItem instances
        for item in project_items:
            # Replace 'http://danpoynor.com.localhost/wp-content/uploads/' with 'images/uploads-all-sizes/' in html_content
            item.html_content = item.html_content.replace('http://danpoynor.com.localhost/wp-content/uploads/', 'images/uploads-all-sizes/')
            # Replace '/wp-content/themes/danpoynor-2017/images/adteractive-email-images/' with '/static/portfolio/images/adteractive-email-images/' in html_content
            item.html_content = item.html_content.replace('/wp-content/themes/danpoynor-2017/images/', '/static/images/')
            # Replace '/static/portfolio/images/adteractive-email-images/adteractive-landing-page-images/' with '/static/portfolio/images/adteractive-landing-page-images/' in html_content
            item.html_content = item.html_content.replace('/static/portfolio/images/adteractive-email-images/adteractive-landing-page-images/', '/static/portfolio/images/adteractive-landing-page-images/')
            # Save the ProjectItem instance
            item.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated html_content field of ProjectItem instances'))
