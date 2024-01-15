from django.contrib.sitemaps import Sitemap
from django.core.paginator import Paginator
from django.urls import reverse
from .constants import PAGINATE_BY

from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem


class BaseSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.5


class StaticViewSitemap(BaseSitemap, Sitemap):
    def items(self):
        return ['home', 'portfolio', 'about', 'contact', 'client_list', 'industry_list', 'market_list', 'mediatype_list', 'role_list']

    def location(self, item):
        return reverse(item)


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

    def location(self, item):
        return item

    def lastmod(self, item):
        return item[1]


class ClientSitemap(BaseSitemap, PaginatedSitemapMixin, Sitemap):
    def get_queryset(self):
        return Client.objects.filter(visible=True)

    def get_detail_url_name(self):
        return 'client_detail'

    def get_page_order_url_name(self):
        return 'client_page_order'


class IndustrySitemap(BaseSitemap, PaginatedSitemapMixin, Sitemap):
    def get_queryset(self):
        return Industry.objects.filter(visible=True)

    def get_detail_url_name(self):
        return 'industry_detail'

    def get_page_order_url_name(self):
        return 'industry_page_order'


class MarketSitemap(BaseSitemap, PaginatedSitemapMixin, Sitemap):
    def get_queryset(self):
        return Market.objects.filter(visible=True)

    def get_detail_url_name(self):
        return 'market_detail'

    def get_page_order_url_name(self):
        return 'market_page_order'


class MediaTypeSitemap(BaseSitemap, PaginatedSitemapMixin, Sitemap):
    def get_queryset(self):
        return MediaType.objects.filter(visible=True)

    def get_detail_url_name(self):
        return 'mediatype_detail'

    def get_page_order_url_name(self):
        return 'mediatype_page_order'


class RoleSitemap(BaseSitemap, PaginatedSitemapMixin, Sitemap):
    def get_queryset(self):
        return Role.objects.filter(visible=True)

    def get_detail_url_name(self):
        return 'role_detail'

    def get_page_order_url_name(self):
        return 'role_page_order'


class ProjectSitemap(BaseSitemap, Sitemap):
    def items(self):
        # Get all the visible projects
        projects = Project.objects.filter(visible=True)

        # Create a Paginator for the projects
        paginator = Paginator(projects, PAGINATE_BY)

        # Create a list to store all the URLs
        urls = []

        # Add the default page URL to the list
        urls.append((reverse('project_list'), projects.latest('updated_at').updated_at))

        # For each page in the paginator
        for page_number in paginator.page_range:
            # For each order
            for order in ['asc', 'desc']:
                # Generate the URL for the page and add it to the list
                urls.append((reverse('projects_page_order', kwargs={'page': page_number, 'order': order}), projects.latest('updated_at').updated_at))

        return urls

    def location(self, item):
        return item[0]

    def lastmod(self, item):
        return item[1]


class ProjectItemDetailSitemap(BaseSitemap, Sitemap):
    def items(self):
        return ProjectItem.objects.filter(visible=True)

    def location(self, item):
        return reverse('project_detail', args=[item.slug])

    def lastmod(self, item):
        return item.updated_at


# Do no include these pages because they have similar content to the /project-detail/ pages.
# For example http://localhost:8000/portfolio/design-and-development-projects/bactrack-breathalyzers-website-redesign/
# class ProjectItemsSitemap(BaseSitemap, Sitemap):
#     def items(self):
#         return ProjectItem.objects.filter(visible=True)

#     def location(self, item):
#         return reverse('project_items_detail', args=[item.slug])

#     def lastmod(self, item):
#         return item.updated_at
