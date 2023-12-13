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
                # print(f"Created new {model.__name__} instance with slug '{slug}'")
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

                # print(f"Processing term with slug '{slug}'")

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

            # print(f"Processing item with post name '{post_name}'")

            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else ''

            description_elem = item.find('description')
            description = description_elem.text if description_elem is not None else ''

            # Ultimately, we want to get the 'content:encoded' element, but using this code does not work for some reason:
            # content_encoded_elem = item.find('content:encoded', namespaces)
            # The 'content:encoded' element is in a namespace, but the namespace might not be defined in the XML file itself.
            # Therefore, we use a wildcard '*' for the namespace to match any 'encoded' element, regardless of its namespace.
            # This will ensure that we find the 'encoded' element even if its namespace is not recognized correctly.
            content_encoded_elem = item.find('{*}encoded')
            if content_encoded_elem is not None:
                content_encoded = content_encoded_elem.text
            else:
                content_encoded = ''
                print(f"Did not find content:encoded element for '{title}'")

            # Try to get the item order from the wp:menu_order element
            item_order_elem = item.find('wp:menu_order', namespaces)
            item_order = int(item_order_elem.text) if item_order_elem is not None else 0

            # Find the project category for the item
            # Try to get the Project instance with this slug
            project_category_elem = item.find(".//category[@domain='project']", namespaces)
            if project_category_elem is not None:
                project_slug = project_category_elem.get('nicename')
                # print(f"Fetching Project with slug '{project_slug}'")
                # Try to get the Project instance with the slug
                project = Project.objects.get(slug=project_slug)

                # Find the taxonomy categories for the item
                # Try to get the model instances with these slugs
                for taxonomy in ['client', 'industry', 'market', 'platform', 'role']:
                    category_elems = item.findall(f".//category[@domain='{taxonomy}']", namespaces)
                    for category_elem in category_elems:
                        category_slug = category_elem.get('nicename')
                        # print(f"Fetching {taxonomy.capitalize()} with slug '{category_slug}'")
                        # Try to get the model instance with the slug
                        if taxonomy == 'platform':
                            # If the taxonomy is 'platform', get the MediaType instance
                            category_instance = MediaType.objects.get(slug=category_slug)
                            # Add the category instance to the project's 'mediatypes' field
                            project.mediatype.add(category_instance)
                        else:
                            category_instance = globals()[taxonomy.capitalize()].objects.get(slug=category_slug)
                            # Add the category instance to the project's many-to-many field
                            if taxonomy == 'client':
                                project.client = category_instance
                            else:
                                getattr(project, f"{taxonomy}").add(category_instance)

                # Find the year for the item
                # Try to get the year from the wp:postmeta element
                year_elem = item.find(".//wp:postmeta[wp:meta_key='_project_year']/wp:meta_value", namespaces)
                if year_elem is not None:
                    year = year_elem.text
                    # print(f"Setting year to '{year}'")
                    # Set the year of the project item
                    project.year = year

                project.save()

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
                    'item_order': item_order,
                },
            )

            if created:
                project_item.save()

        if not error_occurred:
            print('Data imported successfully.')
