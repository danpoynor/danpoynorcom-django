from django.core.management.base import BaseCommand
from portfolio.models import Client, Industry, Market, MediaType, Role, Project, ProjectItem
import xml.etree.ElementTree as ET


class Command(BaseCommand):
    help = 'Imports data from a WordPress XML file'

    def handle(self, *args, **options):
        # Parse the XML file
        try:
            tree = ET.parse('./portfolio/fixtures/danpoynor.WordPress.2023-12-06.xml')
        except ET.ParseError as e:
            self.stdout.write(self.style.ERROR(f"Error parsing XML file: {e}"))
            return

        root = tree.getroot()

        # Namespace dictionary to find the tags
        namespaces = {'wp': 'http://wordpress.org/export/1.2/'}

        # Function to get or create a model instance
        def get_or_create_instance(model, name, description, slug):
            instance, created = model.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': description},
            )
            if created:
                print(f"Created new {model.__name__} instance with slug '{slug}'")
                instance.save()
            return instance

        # Iterate over the XML data
        error_occurred = False
        for term in root.findall('.//wp:term', namespaces):
            try:
                # Check if term elements exists before accessing their text attribute
                term_taxonomy_elem = term.find('wp:term_taxonomy', namespaces)
                taxonomy = term_taxonomy_elem.text if term_taxonomy_elem is not None else ''

                term_slug_elem = term.find('wp:term_slug', namespaces)
                slug = term_slug_elem.text if term_slug_elem is not None else ''

                term_name_elem = term.find('wp:term_name', namespaces)
                name = term_name_elem.text if term_name_elem is not None else ''

                term_description_elem = term.find('wp:term_description', namespaces)
                description = term_description_elem.text if term_description_elem is not None else ''

                print(f"Processing term with slug '{slug}'")

                # Depending on the taxonomy, get or create a new instance of the appropriate model
                try:
                    if taxonomy == 'client':
                        get_or_create_instance(Client, name, description, slug)
                    elif taxonomy == 'industry':
                        get_or_create_instance(Industry, name, description, slug)
                    elif taxonomy == 'market':
                        get_or_create_instance(Market, name, description, slug)
                    elif taxonomy == 'platform':
                        get_or_create_instance(MediaType, name, description, slug)
                    elif taxonomy == 'role':
                        get_or_create_instance(Role, name, description, slug)
                    elif taxonomy == 'project':
                        get_or_create_instance(Project, name, description, slug)
                except Exception as e:
                    print(f"Error saving model instance: {e}")
                    error_occurred = True
            except Exception as e:
                print(f"Error saving model instance for term '{name}' with slug '{slug}': {e}")
                error_occurred = True

        # Process the ProjectItem model in a separate loop
        for item in root.findall(".//item[wp:post_type='dpportfolio']", namespaces):
            post_name_elem = item.find('wp:post_name', namespaces)
            post_name = post_name_elem.text if post_name_elem is not None else ''

            print(f"Processing item with post name '{post_name}'")

            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else ''

            description_elem = item.find('description')
            description = description_elem.text if description_elem is not None else ''

            content_encoded_elem = item.find('content:encoded')
            content_encoded = content_encoded_elem.text if content_encoded_elem is not None else ''

            # Find the project category for the item
            # Try to get the Project instance with this slug
            project_category_elem = item.find(".//category[@domain='project']", namespaces)
            if project_category_elem is not None:
                project_slug = project_category_elem.get('nicename')
                print(f"Fetching Project with slug '{project_slug}'")
                # Try to get the Project instance with the slug
                project = Project.objects.get(slug=project_slug)

            # Find the wp:meta_value element that has a sibling wp:meta_key element with text _wp_old_slug
            for meta in item.findall(".//wp:postmeta", namespaces):
                meta_key_elem = meta.find('wp:meta_key', namespaces)
                if meta_key_elem is not None and meta_key_elem.text == '_wp_old_slug':
                    meta_value_elem = meta.find('wp:meta_value', namespaces)
                    if meta_value_elem is not None:
                        post_name = meta_value_elem.text
                        break

            project_item, created = ProjectItem.objects.get_or_create(
                slug=post_name,
                defaults={
                    'project': project,
                    'name': title,
                    'description': description,
                    'html_content': content_encoded,
                },
            )
            if created:
                project_item.save()

        if not error_occurred:
            print('Data imported successfully.')
