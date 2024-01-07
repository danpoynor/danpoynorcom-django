"""
To run the tests in this file, use the following command:

python manage.py test portfolio.tests.test_urls

This command tells Django to run the tests in the 'test_urls' module of the 'tests' package in the 'portfolio' app.

Make sure to replace 'portfolio' with the actual name of your Django app if it's different.

You can also use the '-k' option followed by the test method name to run a specific test. For example:

python manage.py test portfolio.tests.test_urls -k test_home_url

This command will only run the 'test_home_url' test.
"""
from django.test import TestCase
from django.urls import reverse, resolve
from portfolio import views


class TestUrls(TestCase):
    def test_home_url(self):
        path = reverse('home')
        self.assertEqual(resolve(path).func, views.home)

    def test_portfolio_url(self):
        path = reverse('portfolio')
        self.assertEqual(resolve(path).func, views.portfolio)

    def test_about_url(self):
        path = reverse('about')
        self.assertEqual(resolve(path).func, views.about)

    def test_contact_url(self):
        path = reverse('contact')
        self.assertEqual(resolve(path).func, views.contact)

    def test_clients_url(self):
        path = reverse('clients')
        self.assertEqual(resolve(path).func, views.clients)

    def test_client_detail_url(self):
        path = reverse('client_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.ClientProjectsListView.as_view().__name__)

    def test_client_page_order_url(self):
        path = reverse('client_page_order', kwargs={'slug': 'test-slug', 'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.ClientProjectsListView.as_view().__name__)

    def test_industries_url(self):
        path = reverse('industries')
        self.assertEqual(resolve(path).func, views.industries)

    def test_industry_detail_url(self):
        path = reverse('industry_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.IndustryProjectsListView.as_view().__name__)

    def test_industry_page_order_url(self):
        path = reverse('industry_page_order', kwargs={'slug': 'test-slug', 'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.IndustryProjectsListView.as_view().__name__)

    def test_markets_url(self):
        path = reverse('markets')
        self.assertEqual(resolve(path).func, views.markets)

    def test_market_detail_url(self):
        path = reverse('market_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.MarketProjectsListView.as_view().__name__)

    def test_market_page_order_url(self):
        path = reverse('market_page_order', kwargs={'slug': 'test-slug', 'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.MarketProjectsListView.as_view().__name__)

    def test_mediatypes_url(self):
        path = reverse('mediatypes')
        self.assertEqual(resolve(path).func, views.mediatypes)

    def test_mediatype_detail_url(self):
        path = reverse('mediatype_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.MediaTypeProjectsListView.as_view().__name__)

    def test_mediatype_page_order_url(self):
        path = reverse('mediatype_page_order', kwargs={'slug': 'test-slug', 'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.MediaTypeProjectsListView.as_view().__name__)

    def test_roles_url(self):
        path = reverse('roles')
        self.assertEqual(resolve(path).func, views.roles)

    def test_role_detail_url(self):
        path = reverse('role_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.RoleProjectsListView.as_view().__name__)

    def test_role_page_order_url(self):
        path = reverse('role_page_order', kwargs={'slug': 'test-slug', 'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.RoleProjectsListView.as_view().__name__)

    def test_projects_url(self):
        path = reverse('projects')
        self.assertEqual(resolve(path).func.__name__, views.ProjectsView.as_view().__name__)

    def test_projects_page_url(self):
        path = reverse('projects_page', kwargs={'page': 1})
        self.assertEqual(resolve(path).func.__name__, views.ProjectsView.as_view().__name__)

    def test_projects_page_order_url(self):
        path = reverse('projects_page_order', kwargs={'page': 1, 'order': 'test-order'})
        self.assertEqual(resolve(path).func.__name__, views.ProjectsView.as_view().__name__)

    def test_projects_page_order_slug_url(self):
        path = reverse('projects_page_order_slug', kwargs={'page': 1, 'order': 'test-order', 'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.ProjectsView.as_view().__name__)

    def test_project_url(self):
        path = reverse('project', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.ProjectItemsView.as_view().__name__)

    def test_project_detail_url(self):
        path = reverse('project_detail', kwargs={'slug': 'test-slug'})
        self.assertEqual(resolve(path).func.__name__, views.ProjectDetailsView.as_view().__name__)
