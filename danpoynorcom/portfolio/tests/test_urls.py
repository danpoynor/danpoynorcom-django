from django.test import TestCase
from django.urls import reverse, resolve
from portfolio import views


class TestUrls(TestCase):
    def test_home_url(self):
        path = reverse('home')
        self.assertEqual(resolve(path).func.__name__, views.HomeView.as_view().__name__)

    def test_portfolio_url(self):
        path = reverse('portfolio')
        self.assertEqual(resolve(path).func.__name__, views.PortfolioView.as_view().__name__)

    def test_about_url(self):
        path = reverse('about')
        self.assertEqual(resolve(path).func.__name__, views.AboutView.as_view().__name__)

    def test_contact_url(self):
        path = reverse('contact')
        self.assertEqual(resolve(path).func.__name__, views.ContactView.as_view().__name__)

    def test_clients_url(self):
        path = reverse('client_list')
        self.assertEqual(resolve(path).func.__name__, views.ContactView.as_view().__name__)

    def test_client_detail_url(self):
        path = reverse('client_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.ClientProjectsListView.as_view().__name__)

    def test_client_page_order_url(self):
        path = reverse('client_page_order', kwargs={'slug': 'test-slug', 'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.ClientProjectsListView.as_view().__name__)

    def test_industries_url(self):
        path = reverse('industry_list')
        self.assertEqual(resolve(path).func.__name__, views.IndustriesView.as_view().__name__)

    def test_industry_detail_url(self):
        path = reverse('industry_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.IndustryProjectsListView.as_view().__name__)

    def test_industry_page_order_url(self):
        path = reverse('industry_page_order', kwargs={'slug': 'test-slug', 'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.IndustryProjectsListView.as_view().__name__)

    def test_markets_url(self):
        path = reverse('market_list')
        self.assertEqual(resolve(path).func.__name__, views.MarketsView.as_view().__name__)

    def test_market_detail_url(self):
        path = reverse('market_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.MarketProjectsListView.as_view().__name__)

    def test_market_page_order_url(self):
        path = reverse('market_page_order', kwargs={'slug': 'test-slug', 'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.MarketProjectsListView.as_view().__name__)

    def test_mediatypes_url(self):
        path = reverse('mediatype_list')
        self.assertEqual(resolve(path).func.__name__, views.MediaTypesView.as_view().__name__)

    def test_mediatype_detail_url(self):
        path = reverse('mediatype_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.MediaTypeProjectsListView.as_view().__name__)

    def test_media_type_page_order_url(self):
        path = reverse('media_type_page_order', kwargs={'slug': 'test-slug', 'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.MediaTypeProjectsListView.as_view().__name__)

    def test_roles_url(self):
        path = reverse('role_list')
        self.assertEqual(resolve(path).func.__name__, views.RolesView.as_view().__name__)

    def test_role_detail_url(self):
        path = reverse('role_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.RoleProjectsListView.as_view().__name__)

    def test_role_page_order_url(self):
        path = reverse('role_page_order', kwargs={'slug': 'test-slug', 'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.RoleProjectsListView.as_view().__name__)

    def test_projects_url(self):
        path = reverse('project_list')
        self.assertEqual(resolve(path).func.__name__, views.ProjectsView.as_view().__name__)

    def test_projects_page_order_url(self):
        path = reverse('projects_page_order', kwargs={'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.ProjectsView.as_view().__name__)

    def test_project_url(self):
        path = reverse('project_items_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.ProjectItemsView.as_view().__name__)

    def test_project_detail_url(self):
        path = reverse('project_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.ProjectDetailsView.as_view().__name__)
