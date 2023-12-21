from django.core.management.base import BaseCommand
from portfolio.models import Client, Industry, Market, MediaType, Role, Project, ProjectItem, ProjectItemImage, ProjectItemAttachment
import xml.etree.ElementTree as ET
import phpserialize


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

        # Iterate over the XML for taxonomy term data
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

        # ProjectItems
        # Process the ProjectItem model in a separate loop
        for item in root.findall(".//item[wp:post_type='dpportfolio']", namespaces):
            post_name_elem = item.find('wp:post_name', namespaces)
            post_name = post_name_elem.text if post_name_elem is not None else ''

            # print(f"Processing item with post name '{post_name}'")

            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else ''

            description_elem = item.find('description')
            description = description_elem.text if description_elem is not None else ''

            # Ultimately, we want to get the 'content:encoded' element, but using this next line does not work for some reason:
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

            # Handle attachments (usually PDF files)
            # Find the <wp:postmeta> child elements with the <wp:meta_key> text 'PDF File' and 'PDF File Link Text'
            attachment_file_elem = item.find(".//wp:postmeta[wp:meta_key='PDF File']/wp:meta_value", namespaces)
            attachment_file_link_text_elem = item.find(".//wp:postmeta[wp:meta_key='PDF File Link Text']/wp:meta_value", namespaces)

            # Get the text of the <wp:meta_value> child elements
            attachment_file = attachment_file_elem.text if attachment_file_elem is not None else ''
            attachment_file = attachment_file.replace('/wp-content/uploads/', '')
            attachment_file_link_text = attachment_file_link_text_elem.text if attachment_file_link_text_elem is not None else ''

            # Create a new ProjectItemAttachment instance with this data only if attachment_file is not an empty string
            if attachment_file:
                attachment = ProjectItemAttachment.objects.create(
                    project_item=project_item,
                    file=attachment_file,
                    link_text=attachment_file_link_text,
                )
                attachment.save()

        # ProjectItemImages
        # Process the ProjectItemImage model in a separate loop
        # First, create a dictionary that maps _thumbnail_id to post_name for dpportfolio items
        thumbnail_id_to_post_name = {}
        for item in root.findall(".//item[wp:post_type='dpportfolio']", namespaces):
            post_name_elem = item.find('wp:post_name', namespaces)
            post_name = post_name_elem.text if post_name_elem is not None else None

            thumbnail_id_elem = item.find(".//wp:postmeta[wp:meta_key='_thumbnail_id']/wp:meta_value", namespaces)
            thumbnail_id = int(thumbnail_id_elem.text) if thumbnail_id_elem is not None else None

            if post_name and thumbnail_id:
                thumbnail_id_to_post_name[thumbnail_id] = post_name

        # Then, in the image import loop, use this dictionary to get the post_name
        for item in root.findall(".//item[wp:post_type='attachment']", namespaces):
            post_id_elem = item.find('wp:post_id', namespaces)
            post_id = int(post_id_elem.text) if post_id_elem is not None else None

            post_name = thumbnail_id_to_post_name.get(post_id)
            if post_name is None:
                print(f"No dpportfolio item found with _thumbnail_id '{post_id}', skipping this attachment")
                continue

            # Get the ProjectItem with the slug that matches post_name
            try:
                project_item = ProjectItem.objects.get(slug=post_name)
            except ProjectItem.DoesNotExist:
                print(f"No ProjectItem found with slug '{post_name}'")
                continue

            # Get the attachment URL, which is the URL of the original image
            attachment_url_elem = item.find('wp:attachment_url', namespaces)
            attachment_url = attachment_url_elem.text if attachment_url_elem is not None else ''
            attachment_url = attachment_url.replace('http://danpoynor.com.localhost/wp-content/uploads/', '')

            # Get the metadata, which contains the URLs of the different image sizes
            metadata_elem = item.find(".//wp:postmeta[wp:meta_key='_wp_attachment_metadata']/wp:meta_value", namespaces)
            if metadata_elem is not None:
                # The metadata is a serialized PHP array, so we need to deserialize it
                metadata = phpserialize.loads(metadata_elem.text.encode(), decode_strings=True)

                # Get the URLs of the different image sizes
                thumbnail_url = metadata['sizes']['thumbnail']['file'] if 'thumbnail' in metadata['sizes'] else ''
                medium_url = metadata['sizes']['medium']['file'] if 'medium' in metadata['sizes'] else ''
                medium_large_url = metadata['sizes']['medium_large']['file'] if 'medium_large' in metadata['sizes'] else ''
                large_url = metadata['sizes']['large']['file'] if 'large' in metadata['sizes'] else ''
                admin_list_thumb_url = metadata['sizes']['admin-list-thumb']['file'] if 'admin-list-thumb' in metadata['sizes'] else ''

                # Create a new ProjectItemImage instance with this data
                image = ProjectItemImage.objects.create(
                    project_item=project_item,
                    original=attachment_url,
                    thumbnail=thumbnail_url,
                    medium=medium_url,
                    medium_large=medium_large_url,
                    large=large_url,
                    admin_list_thumb=admin_list_thumb_url,
                )
                image.save()

        if not error_occurred:
            print('Data imported successfully.')
