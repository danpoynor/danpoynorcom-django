import os
import json
import logging
from os import stat
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.core.cache import cache
from django.core.paginator import Paginator
# from ..models import Client, Industry, Market, MediaType, Role, Project, ProjectItem
from ..constants import VIEW_NAMES, MODELS

# MODELS = [Client, Industry, Market, MediaType, Role, Project, ProjectItem]

# Create a logger
logger = logging.getLogger(__name__)


class WebsiteSeoView(View):
    def get(self, request, *args, **kwargs):
        # Build the list of URLs
        # NOTE: VIEW_NAMES are the same names used in the urls.py file and used here in
        # the reverse() function for BeautifulSoup to get the URLs and parse the data.
        # MODELS are the same models used in the models.py file and used here to get the
        # absolute URLs for each object.
        urls = [request.build_absolute_uri(reverse(view_name)) for view_name in VIEW_NAMES]
        for model in MODELS:
            urls.extend(request.build_absolute_uri(obj.get_absolute_url()) for obj in model.visible_objects.all())

        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Construct the absolute path to the JSON file in the
        # danpoynorcom-django/danpoynorcom/portfolio/output/ directory
        parent_dir_path = os.path.dirname(dir_path)
        json_file_path = os.path.join(parent_dir_path, 'output', 'seo_data.json')

        # Fetch and save the data when the refresh button is clicked
        if 'refresh_seo_data' in request.GET:
            logger.info("====> Refreshing SEO data. This could take a while...")
            seo_data = []
            for url in urls:
                # Try to get the data from the cache
                data = cache.get(f'seo_data_{url}')

                # If the data is not in the cache, fetch it from the web page
                if not data:
                    try:
                        response = requests.get(url, timeout=20)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title = str(soup.title.string) if soup.title else ''
                        description_tag = soup.find('meta', attrs={'name': 'description'})
                        description = str(description_tag['content']) if description_tag else ''
                        h1_tags = [str(tag.get_text(strip=True)) for tag in soup.find_all('h1')]
                        word_count = len(soup.get_text().split())
                        data = {
                            'url': url,
                            'title': title,
                            'description': description,
                            'h1_tags': h1_tags,
                            'word_count': word_count,
                        }
                        cache.set(f'seo_data_{url}', data, 3600)  # Cache the data for 1 hour
                    except requests.exceptions.RequestException as e:
                        print(f'Error fetching {url}: {e}')
                        continue

                seo_data.append(data)

            # Save the data to a JSON file
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(seo_data, f)

        # Initialize last_modified with a default value
        last_modified = None

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                seo_data = json.load(f)
                logger.info("==========> SEO data found at %s", json_file_path)
                # Get the last modified date of the JSON file
                timestamp = stat(json_file_path).st_mtime
                last_modified = datetime.fromtimestamp(timestamp)
                # Format the date to include the day of the week
                last_modified = last_modified.strftime('%A, %B %d, %Y, %H:%M:%S')
        except FileNotFoundError:
            seo_data = []
            logger.info("==========> SEO data NOT found at %s", json_file_path)

        # Get the total number of items before filtering
        seo_data_total_length = len(seo_data)

        # Filter the data based on the search query
        search_query = request.GET.get('search_term', '')  # Default to empty string if not provided
        if search_query:
            seo_data = [item for item in seo_data if search_query.lower() in item['url'].lower() or search_query.lower() in item['title'].lower() or search_query.lower() in item['description'].lower()]

        # Limit the number of items if specified
        total_items = request.GET.get('total_items', 'all')  # Default number of items if not provided
        if total_items != 'all':
            seo_data = seo_data[:int(total_items)]  # Convert to int because GET parameters are always strings

        # Paginate the data
        paginator = Paginator(seo_data, 100)  # Increase PAGINATE_BY to see more results per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Get the total number of items after filtering
        total_items = len(seo_data)

        return render(request, 'seo_overview.html', {'page_obj': page_obj, 'total_items': total_items, 'all_urls': urls, 'seo_data_total_length': seo_data_total_length, 'search_query': search_query, 'last_modified': last_modified})
