from django.contrib.sitemaps import Sitemap
from django.core.paginator import Paginator
from django.urls import reverse
from .constants import PAGINATE_BY
from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem
from .mixins import PaginationMixin


class BaseSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'yearly'
    priority = 0.5


class StaticViewSitemap(BaseSitemap, Sitemap):
    def items(self):
        return ['home', 'portfolio', 'about', 'contact', 'client_list', 'industry_list', 'market_list', 'mediatype_list', 'role_list']

    def location(self, item):
        return reverse(item)


class PaginatedSitemapMixin(PaginationMixin):
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
            projects = item.project_items.filter(visible=True)

            # Create a Paginator for the projects
            paginator = Paginator(projects, PAGINATE_BY)

            # If more than one page in paginator.page_range
            if paginator.num_pages > 1:
                # For each page in the paginator
                for page_number in paginator.page_range:
                    # For each order
                    for order in ['asc', 'desc']:
                        # Generate the URL for the page and add it to the list
                        urls.append(reverse(self.get_page_order_url_name(), kwargs={'slug': item.slug, 'page': page_number, 'order': order}))

        return urls

    def location(self, item):
        return item

        if item[1] is not None:
            try:
                return item[1].date()
            except (ValueError, AttributeError):
                pass
        return None


class ClientSitemap(BaseSitemap, PaginatedSitemapMixin, Sitemap):
    def get_queryset(self):
        return Client.visible_objects.filter(visible=True)

    def get_detail_url_name(self):
        return 'client_detail'

    def get_page_order_url_name(self):
        return 'client_page_order'


class IndustrySitemap(BaseSitemap, PaginatedSitemapMixin, Sitemap):
    def get_queryset(self):
        return Industry.visible_objects.filter(visible=True)

    def get_detail_url_name(self):
        return 'industry_detail'

    def get_page_order_url_name(self):
        return 'industry_page_order'


class MarketSitemap(BaseSitemap, PaginatedSitemapMixin, Sitemap):
    def get_queryset(self):
        return Market.visible_objects.filter(visible=True)

    def get_detail_url_name(self):
        return 'market_detail'

    def get_page_order_url_name(self):
        return 'market_page_order'


class MediaTypeSitemap(BaseSitemap, PaginatedSitemapMixin, Sitemap):
    def get_queryset(self):
        return MediaType.visible_objects.filter(visible=True)

    def get_detail_url_name(self):
        return 'mediatype_detail'

    def get_page_order_url_name(self):
        return 'media_type_page_order'


class RoleSitemap(BaseSitemap, PaginatedSitemapMixin, Sitemap):
    def get_queryset(self):
        return Role.visible_objects.filter(visible=True)

    def get_detail_url_name(self):
        return 'role_detail'

    def get_page_order_url_name(self):
        return 'role_page_order'


class ProjectSitemap(BaseSitemap, Sitemap):
    def items(self):
        # Get all the visible projects
        projects = Project.visible_objects.filter(visible=True)

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
        # Ensure item[1] is not None and is a valid date
        if item[1] is not None:
            try:
                return item[1].date()
            except (ValueError, AttributeError):
                pass
        return None


class ProjectItemDetailSitemap(BaseSitemap, Sitemap):
    def items(self):
        return ProjectItem.visible_objects.filter(visible=True)

    def location(self, item):
        return reverse('project_detail', args=[item.slug])

    def lastmod(self, item):
        return item.updated_at


# Do no include these pages because they have similar content to the /project-detail/ pages.
# For example http://localhost:8000/portfolio/design-and-development-projects/bactrack-breathalyzers-website-redesign/
class ProjectItemsSitemap(BaseSitemap, Sitemap):
    def items(self):
        return ProjectItem.visible_objects.filter(visible=True)

    def location(self, item):
        return reverse('project_items_detail', args=[item.slug])

    def lastmod(self, item):
        return item.updated_at
