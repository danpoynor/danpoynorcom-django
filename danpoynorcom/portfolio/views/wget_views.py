from django.http import HttpResponse
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse
from ..constants import PAGINATE_BY
from ..models import Client, Industry, Market, MediaType, Role, Project, ProjectItem


class PaginatedSitemapMixin:
    def get_queryset(self):
        raise NotImplementedError

    def get_detail_url_name(self):
        raise NotImplementedError

    def get_page_order_url_name(self):
        raise NotImplementedError

    def items(self):
        # Get all the items
        items = self.get_queryset()

        # Create a list to store all the URLs
        urls = []

        # For each item
        for item in items:
            # Generate the URL for the default page and add it to the list
            urls.append(reverse(self.get_detail_url_name(), kwargs={'slug': item.slug}))

            # Get all the visible projects for the item
            projects = item.projects.filter(visible=True)

            # Create a Paginator for the projects
            paginator = Paginator(projects, PAGINATE_BY)

            # For each page in the paginator
            for page_number in paginator.page_range:
                # For each order
                for order in ['asc', 'desc']:
                    # Generate the URL for the page and add it to the list
                    urls.append(reverse(self.get_page_order_url_name(), kwargs={'slug': item.slug, 'page': page_number, 'order': order}))

        return urls


class WgetSitemapView(View):
    sitemaps = [
        {
            'queryset': Client.objects.filter(visible=True),
            'detail_url_name': 'client_detail',
            'page_order_url_name': 'client_page_order',
        },
        {
            'queryset': Industry.objects.filter(visible=True),
            'detail_url_name': 'industry_detail',
            'page_order_url_name': 'industry_page_order',
        },
        {
            'queryset': Market.objects.filter(visible=True),
            'detail_url_name': 'market_detail',
            'page_order_url_name': 'market_page_order',
        },
        {
            'queryset': MediaType.objects.filter(visible=True),
            'detail_url_name': 'mediatype_detail',
            'page_order_url_name': 'mediatype_page_order',
        },
        {
            'queryset': Role.objects.filter(visible=True),
            'detail_url_name': 'role_detail',
            'page_order_url_name': 'role_page_order',
        },
        {
            'queryset': Project.objects.filter(visible=True),
            'detail_url_name': 'project_detail',
        },
        {
            'queryset': ProjectItem.objects.filter(visible=True),
            'detail_url_name': 'project_items_detail',
        },
    ]

    def items(self):
        # Get the URLs for the static views
        static_urls = [reverse(view_name) for view_name in ['home', 'portfolio', 'about', 'contact', 'client_list', 'industry_list', 'market_list', 'mediatype_list', 'role_list']]

        # Create a list to store all the URLs
        urls = []

        # For each sitemap
        for sitemap in self.sitemaps:
            # Get all the items
            items = sitemap['queryset']

            # For each item
            for item in items:
                # Generate the URL for the default page and add it to the list
                urls.append(reverse(sitemap['detail_url_name'], kwargs={'slug': item.slug}))

                # If the model has pagination
                if 'page_order_url_name' in sitemap:
                    # Get all the visible projects for the item
                    projects = item.projects.filter(visible=True)

                    # Create a Paginator for the projects
                    paginator = Paginator(projects, PAGINATE_BY)

                    # Only generate URLs for additional pages if there's more than one page
                    if paginator.num_pages > 1:
                        # For each page in the paginator
                        for page_number in paginator.page_range:
                            # For each order
                            for order in ['asc', 'desc']:
                                # Generate the URL for the page and add it to the list
                                urls.append(reverse(sitemap['page_order_url_name'], kwargs={'slug': item.slug, 'page': page_number, 'order': order}))

        # Combine the two lists
        return static_urls + urls

    def get(self, request, *args, **kwargs):
        urls = self.items()
        response = HttpResponse('\n'.join(urls), content_type='text/plain')
        return response
