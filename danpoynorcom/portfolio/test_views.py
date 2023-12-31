import unittest
from django.urls import reverse
from django.test import TestCase
from portfolio.models import Project, ProjectItem, Client, Industry, Market, MediaType, Role
from portfolio.views import ClientProjectsListView
import pdb

# Run tests with one of these commands:
# `python manage.py test portfolio`
# `python manage.py test portfolio.tests.test_views`


class ProjectsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        number_of_projects = 5
        client = Client.objects.create(name='Test Client', visible=True)
        industry = Industry.objects.create(name='Test Industry', visible=True)
        market = Market.objects.create(name='Test Market', visible=True)
        media_type = MediaType.objects.create(name='Test MediaType', visible=True)
        role = Role.objects.create(name='Test Role', visible=True)
        for project_id in range(number_of_projects):
            project = Project.objects.create(
                name=f'Project {project_id}',
                slug=f'project-{project_id}',
                visible=True,
                client=client,
            )
            # print(project.slug)  # Print the slug value
            project.industry.set([industry])
            project.market.set([market])
            project.mediatype.set([media_type])
            project.role.set([role])
            ProjectItem.objects.create(
                project=project,
                slug=f'project-item-{project_id}',
                visible=True,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/portfolio/design-and-development-projects/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/design-and-development-projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/portfolio/projects/page.html')

    def test_post_redirects_to_first_page_with_selected_order(self):
        response = self.client.post('/portfolio/design-and-development-projects/', {'order': 'desc'})
        self.assertRedirects(response, '/portfolio/design-and-development-projects/page/1/desc/')

    def test_get_context_data(self):
        response = self.client.get('/portfolio/design-and-development-projects/page/1/asc/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('order' in response.context)
        self.assertTrue('pages' in response.context)
        self.assertTrue('total_projects' in response.context)
        self.assertTrue('count_type' in response.context)
        self.assertEqual(response.context['view_name'], 'projects_page_order')
        self.assertEqual(response.context['taxonomy_item_slug'], '')

    def test_pagination(self):
        response = self.client.get('/portfolio/design-and-development-projects/page/1/asc/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('order' in response.context)
        self.assertTrue('pages' in response.context)
        self.assertTrue('total_projects' in response.context)
        self.assertTrue('count_type' in response.context)
        self.assertEqual(response.context['page_obj'].number, 1)
        self.assertEqual(response.context['order'], 'asc')
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 1)  # Check the total number of pages
        self.assertEqual(response.context['total_projects'], 5)
        self.assertEqual(response.context['count_type'], 'projects')
        self.assertEqual(response.context['view_name'], 'projects_page_order')
        self.assertEqual(response.context['taxonomy_item_slug'], '')


class ProjectItemsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        client = Client.objects.create(name='Test Client', slug='test-client')
        project = Project.objects.create(name='Test Project', slug='test-project', client=client)
        ProjectItem.objects.create(name='Test ProjectItem 1', slug='test-projectitem-1', project=project, visible=True)
        ProjectItem.objects.create(name='Test ProjectItem 2', slug='test-projectitem-2', project=project, visible=False)
        ProjectItem.objects.create(name='Test ProjectItem 3', slug='test-projectitem-3', project=project, visible=True)

    def test_view_url_exists_at_desired_location(self):
        project = Project.objects.get(slug='test-project')
        response = self.client.get(f'/portfolio/design-and-development-projects/{project.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        project = Project.objects.get(slug='test-project')
        response = self.client.get(f'/portfolio/design-and-development-projects/{project.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/portfolio/projects/project_items.html')

    def test_context_data(self):
        project = Project.objects.get(slug='test-project')
        response = self.client.get(f'/portfolio/design-and-development-projects/{project.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('items' in response.context)
        items = response.context['items']
        self.assertEqual(items.count(), 2)
        self.assertTrue(all(item.visible for item in items))

    def test_nonexistent_projectitem(self):
        response = self.client.get('/portfolio/design-and-development-projects/nonexistent-projectitem/')
        self.assertEqual(response.status_code, 404)


class ProjectDetailsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        client = Client.objects.create(name='Test Client', slug='test-client')
        project = Project.objects.create(name='Test Project', slug='test-project', client=client)
        project_item = ProjectItem.objects.create(name='Test Project Item', slug='test-project-item', project=project, visible=True)

    def test_view_url_exists_at_desired_location(self):
        project_item = ProjectItem.objects.get(slug='test-project-item')
        response = self.client.get(f'/portfolio/project-details/{project_item.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        project_item = ProjectItem.objects.get(slug='test-project-item')
        response = self.client.get(f'/portfolio/project-details/{project_item.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/portfolio/projects/project_details.html')

    def test_context_data(self):
        project_item = ProjectItem.objects.get(slug='test-project-item')
        response = self.client.get(f'/portfolio/project-details/{project_item.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('items' in response.context)
        items = response.context['items']
        self.assertEqual(items.count(), 1)
        self.assertTrue(all(item.visible for item in items))

    def test_nonexistent_project_item(self):
        response = self.client.get('/portfolio/project-details/nonexistent-project-item/')
        self.assertEqual(response.status_code, 404)


class ClientProjectsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        client = Client.objects.create(name='Test Client', slug='test-client')
        number_of_projects = 5
        for project_id in range(number_of_projects):
            Project.objects.create(
                name=f'Project {project_id}',
                slug=f'project-{project_id}',
                visible=True,
                client=client,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/portfolio/clients/test-client/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/clients/test-client/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/portfolio/clients/term_items_page.html')

    def test_context_data(self):
        response = self.client.get('/portfolio/clients/test-client/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('order' in response.context)
        self.assertTrue('pages' in response.context)
        self.assertTrue('total_projects' in response.context)
        self.assertTrue('count_type' in response.context)


class IndustryProjectsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        industry = Industry.objects.create(name='Test Industry', slug='test-industry')
        number_of_projects = 5
        for project_id in range(number_of_projects):
            project = Project.objects.create(
                name=f'Project {project_id}',
                slug=f'project-{project_id}',
                visible=True,
            )
            project.industry.add(industry)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/portfolio/industries/test-industry/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/industries/test-industry/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/portfolio/industries/term_items_page.html')

    def test_context_data(self):
        response = self.client.get('/portfolio/industries/test-industry/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('order' in response.context)
        self.assertTrue('pages' in response.context)
        self.assertTrue('total_projects' in response.context)
        self.assertTrue('count_type' in response.context)


class MarketProjectsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        market = Market.objects.create(name='Test Market', slug='test-market')
        number_of_projects = 5
        for project_id in range(number_of_projects):
            project = Project.objects.create(
                name=f'Project {project_id}',
                slug=f'project-{project_id}',
                visible=True,
            )
            project.market.add(market)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/portfolio/markets/test-market/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/markets/test-market/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/portfolio/markets/term_items_page.html')

    def test_context_data(self):
        response = self.client.get('/portfolio/markets/test-market/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('order' in response.context)
        self.assertTrue('pages' in response.context)
        self.assertTrue('total_projects' in response.context)
        self.assertTrue('count_type' in response.context)


class MediaTypeProjectsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        mediatype = MediaType.objects.create(name='Test Media Type', slug='test-mediatype')
        number_of_projects = 5
        for project_id in range(number_of_projects):
            project = Project.objects.create(
                name=f'Project {project_id}',
                slug=f'project-{project_id}',
                visible=True,
            )
            project.mediatype.add(mediatype)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/portfolio/media-types/test-mediatype/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/media-types/test-mediatype/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/portfolio/media_types/term_items_page.html')

    def test_context_data(self):
        response = self.client.get('/portfolio/media-types/test-mediatype/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('order' in response.context)
        self.assertTrue('pages' in response.context)
        self.assertTrue('total_projects' in response.context)
        self.assertTrue('count_type' in response.context)


class RoleProjectsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        role = Role.objects.create(name='Test Role', slug='test-role')
        number_of_projects = 5
        for project_id in range(number_of_projects):
            project = Project.objects.create(
                name=f'Project {project_id}',
                slug=f'project-{project_id}',
                visible=True,
            )
            project.role.add(role)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/portfolio/roles/test-role/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/roles/test-role/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/portfolio/roles/term_items_page.html')

    def test_context_data(self):
        response = self.client.get('/portfolio/roles/test-role/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('order' in response.context)
        self.assertTrue('pages' in response.context)
        self.assertTrue('total_projects' in response.context)
        self.assertTrue('count_type' in response.context)


if __name__ == '__main__':
    unittest.main()
