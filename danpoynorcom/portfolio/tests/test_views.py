import unittest
from django.urls import reverse, resolve
from django.test import TestCase, RequestFactory
from portfolio.models import Project, ProjectItem, Client, Industry, Market, MediaType, Role
from portfolio.views import HomeView, AboutView, ContactView


class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_home_view_uses_correct_template(self):
        request = self.factory.get(reverse('home'))
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'portfolio/home.html')

    def test_home_view_has_correct_title_in_context(self):
        request = self.factory.get(reverse('home'))
        response = HomeView.as_view()(request)
        self.assertEqual(response.context_data['title'], 'Dan Poynor : Visual / UX / Web Design & Development : Austin, TX')

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomeView.as_view().__name__)


class AboutViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_about_view_uses_correct_template(self):
        request = self.factory.get(reverse('about'))
        response = AboutView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'portfolio/about.html')

    def test_about_view_has_correct_title_in_context(self):
        request = self.factory.get(reverse('about'))
        response = AboutView.as_view()(request)
        self.assertEqual(response.context_data['title'], 'Dan Poynor : UI/UX Design & Web Development : Austin, TX')

    def test_about_url_resolves_about_view(self):
        view = resolve('/about/')
        self.assertEqual(view.func.__name__, AboutView.as_view().__name__)


class ContactViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_contact_view_uses_correct_template(self):
        request = self.factory.get(reverse('contact'))
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'portfolio/contact.html')

    def test_contact_view_has_correct_title_in_context(self):
        request = self.factory.get(reverse('about'))
        response = ContactView.as_view()(request)
        self.assertEqual(response.context_data['title'], 'Let’s Connect! : UI/UX Design & Web Development : Austin, TX')

    def test_contact_url_resolves_about_view(self):
        view = resolve('/contact/')
        self.assertEqual(view.func.__name__, ContactView.as_view().__name__)


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
        self.assertTemplateUsed(response, 'portfolio/projects_list.html')

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
        self.assertTemplateUsed(response, 'portfolio/project_items_detail.html')

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
        self.assertTemplateUsed(response, 'portfolio/project_details.html')

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
        response = self.client.get('/portfolio/clients/test-client-projects/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/clients/test-client-projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/client_detail.html')

    def test_context_data(self):
        response = self.client.get('/portfolio/clients/test-client-projects/')
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
        response = self.client.get('/portfolio/industries/test-industry-projects/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/industries/test-industry-projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/industry_detail.html')

    def test_context_data(self):
        response = self.client.get('/portfolio/industries/test-industry-projects/')
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
        response = self.client.get('/portfolio/markets/test-market-projects/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/markets/test-market-projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/market_detail.html')

    def test_context_data(self):
        response = self.client.get('/portfolio/markets/test-market-projects/')
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
        mediatype_names = ['Children', 'Test Media Type', 'Designer', 'Displays', 'Aol', 'Specifications', 'Html', 'Pop', 'Videos']
        for name in mediatype_names:
            mediatype = MediaType.objects.create(name=name, slug=name.lower().replace(' ', '-'))
            number_of_projects = 5
            for project_id in range(number_of_projects):
                project = Project.objects.create(
                    name=f'{name} Project {project_id}',
                    slug=f"{name.lower().replace(' ', '-')}-project-{project_id}",
                    visible=True,
                )
                project.mediatype.add(mediatype)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/portfolio/media-types/test-media-type-projects/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/media-types/test-media-type-projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/mediatype_detail.html')

    def test_context_data(self):
        response = self.client.get('/portfolio/media-types/test-media-type-projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('order' in response.context)
        self.assertTrue('pages' in response.context)
        self.assertTrue('total_projects' in response.context)
        self.assertTrue('count_type' in response.context)

    def check_title(self, url, expected_title):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title' in response.context)
        self.assertEqual(response.context['title'], expected_title)

    def test_title_processing(self):
        self.check_title('/portfolio/media-types/children-projects/', 'Child Designer Portfolio : Austin, TX : Page 1 Asc')
        self.check_title('/portfolio/media-types/test-media-type-projects/', 'Test Media Type Designer Portfolio : Austin, TX : Page 1 Asc')
        self.check_title('/portfolio/media-types/designer-projects/', 'Designer Portfolio : Austin, TX : Page 1 Asc')
        self.check_title('/portfolio/media-types/displays-projects/', 'Display Designer Portfolio : Austin, TX : Page 1 Asc')
        self.check_title('/portfolio/media-types/aol-projects/', 'AOL Designer Portfolio : Austin, TX : Page 1 Asc')
        self.check_title('/portfolio/media-types/specifications-projects/', 'Specifications Designer Portfolio : Austin, TX : Page 1 Asc')
        self.check_title('/portfolio/media-types/html-projects/', 'HTML Designer Portfolio : Austin, TX : Page 1 Asc')
        self.check_title('/portfolio/media-types/pop-projects/', 'POP Designer Portfolio : Austin, TX : Page 1 Asc')
        self.check_title('/portfolio/media-types/videos-projects/', 'Video Editing Portfolio : Austin, TX : Page 1 Asc')

    def test_nonexistent_media_type(self):
        response = self.client.get('/portfolio/media-types/nonexistent-projects/')
        self.assertEqual(response.status_code, 404)


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
        response = self.client.get('/portfolio/roles/test-role-projects/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/portfolio/roles/test-role-projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/role_detail.html')

    def test_context_data(self):
        response = self.client.get('/portfolio/roles/test-role-projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('order' in response.context)
        self.assertTrue('pages' in response.context)
        self.assertTrue('total_projects' in response.context)
        self.assertTrue('count_type' in response.context)


if __name__ == '__main__':
    unittest.main()
