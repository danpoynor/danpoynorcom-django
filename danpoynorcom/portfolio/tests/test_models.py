from django.test import TestCase
# NOTE: I'm using PortfolioClient to avoid conflict with django.test.Client
from portfolio.models import Client as PortfolioClient, Industry, Market, MediaType, Role, Project, ProjectItem, ProjectItemImage, ProjectItemAttachment


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        PortfolioClient.objects.create(name='Test Client', slug='test-client', logo='http://example.com/logo.jpg', website='http://example.com')

    def test_name_label(self):
        client = PortfolioClient.objects.get(id=1)
        field_label = client._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        client = PortfolioClient.objects.get(id=1)
        max_length = client._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        client = PortfolioClient.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(client.get_absolute_url(), '/portfolio/clients/test-client-projects/')

    def test_description_is_optional(self):
        client = PortfolioClient.objects.get(id=1)
        self.assertTrue(client._meta.get_field('description').blank)

    def test_visible_defaults_to_true(self):
        client = PortfolioClient.objects.get(id=1)
        self.assertTrue(client.visible)

    def test_logo_max_length(self):
        client = PortfolioClient.objects.get(id=1)
        max_length = client._meta.get_field('logo').max_length
        self.assertEqual(max_length, 200)

    def test_website_max_length(self):
        client = PortfolioClient.objects.get(id=1)
        max_length = client._meta.get_field('website').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        client = PortfolioClient.objects.get(id=1)
        expected_object_name = f'{client.name}'
        self.assertEqual(expected_object_name, str(client))


class IndustryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Industry.objects.create(name='Test Industry', slug='test-industry', image_sm='http://example.com/image_sm.jpg', image_md='http://example.com/image_md.jpg', image_lg='http://example.com/image_lg.jpg')

    def test_name_label(self):
        industry = Industry.objects.get(id=1)
        field_label = industry._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        industry = Industry.objects.get(id=1)
        max_length = industry._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        industry = Industry.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(industry.get_absolute_url(), '/portfolio/industries/test-industry-projects/')

    def test_description_is_optional(self):
        industry = Industry.objects.get(id=1)
        self.assertTrue(industry._meta.get_field('description').blank)

    def test_visible_defaults_to_true(self):
        industry = Industry.objects.get(id=1)
        self.assertTrue(industry.visible)

    def test_image_sm_max_length(self):
        industry = Industry.objects.get(id=1)
        max_length = industry._meta.get_field('image_sm').max_length
        self.assertEqual(max_length, 200)

    def test_image_md_max_length(self):
        industry = Industry.objects.get(id=1)
        max_length = industry._meta.get_field('image_md').max_length
        self.assertEqual(max_length, 200)

    def test_image_lg_max_length(self):
        industry = Industry.objects.get(id=1)
        max_length = industry._meta.get_field('image_lg').max_length
        self.assertEqual(max_length, 200)


class MarketModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Market.objects.create(name='Test Market', slug='test-market', description='Test Description')

    def test_name_label(self):
        market = Market.objects.get(id=1)
        field_label = market._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        market = Market.objects.get(id=1)
        max_length = market._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        market = Market.objects.get(id=1)
        self.assertEqual(market.get_absolute_url(), '/portfolio/markets/test-market-projects/')

    def test_description_is_optional(self):
        market = Market.objects.get(id=1)
        self.assertTrue(market._meta.get_field('description').blank)

    def test_description_content(self):
        market = Market.objects.get(id=1)
        expected_description = 'Test Description'
        self.assertEqual(market.description, expected_description)

    def test_str_method(self):
        market = Market.objects.get(id=1)
        expected_object_name = 'Test Market'
        self.assertEqual(str(market), expected_object_name)


class MediaTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        MediaType.objects.create(name='Test MediaType', slug='test-mediatype', description='Test Description', image_sm='http://example.com/image_sm.jpg', image_md='http://example.com/image_md.jpg', image_lg='http://example.com/image_lg.jpg')

    def test_name_label(self):
        mediatype = MediaType.objects.get(id=1)
        field_label = mediatype._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        mediatype = MediaType.objects.get(id=1)
        max_length = mediatype._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        mediatype = MediaType.objects.get(id=1)
        self.assertEqual(mediatype.get_absolute_url(), '/portfolio/media-types/test-mediatype-projects/')

    def test_description_is_optional(self):
        mediatype = MediaType.objects.get(id=1)
        self.assertTrue(mediatype._meta.get_field('description').blank)

    def test_description_content(self):
        mediatype = MediaType.objects.get(id=1)
        expected_description = 'Test Description'
        self.assertEqual(mediatype.description, expected_description)

    def test_image_sm_max_length(self):
        mediatype = MediaType.objects.get(id=1)
        max_length = mediatype._meta.get_field('image_sm').max_length
        self.assertEqual(max_length, 200)

    def test_image_md_max_length(self):
        mediatype = MediaType.objects.get(id=1)
        max_length = mediatype._meta.get_field('image_md').max_length
        self.assertEqual(max_length, 200)

    def test_image_lg_max_length(self):
        mediatype = MediaType.objects.get(id=1)
        max_length = mediatype._meta.get_field('image_lg').max_length
        self.assertEqual(max_length, 200)

    def test_str_method(self):
        mediatype = MediaType.objects.get(id=1)
        expected_object_name = 'Test MediaType'
        self.assertEqual(str(mediatype), expected_object_name)

    def test_slug_label(self):
        mediatype = MediaType.objects.get(id=1)
        field_label = mediatype._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_slug_max_length(self):
        mediatype = MediaType.objects.get(id=1)
        max_length = mediatype._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)

    def test_visible_defaults_to_true(self):
        mediatype = MediaType.objects.get(id=1)
        self.assertTrue(mediatype.visible)

    def test_image_sm_is_optional(self):
        mediatype = MediaType.objects.get(id=1)
        self.assertTrue(mediatype._meta.get_field('image_sm').blank)

    def test_image_md_is_optional(self):
        mediatype = MediaType.objects.get(id=1)
        self.assertTrue(mediatype._meta.get_field('image_md').blank)

    def test_image_lg_is_optional(self):
        mediatype = MediaType.objects.get(id=1)
        self.assertTrue(mediatype._meta.get_field('image_lg').blank)


class RoleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Role.objects.create(name='Test Role', slug='test-role', description='Test Description', image_sm='http://example.com/image_sm.jpg', image_md='http://example.com/image_md.jpg', image_lg='http://example.com/image_lg.jpg')

    def test_name_label(self):
        role = Role.objects.get(id=1)
        field_label = role._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        role = Role.objects.get(id=1)
        max_length = role._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        role = Role.objects.get(id=1)
        self.assertEqual(role.get_absolute_url(), '/portfolio/roles/test-role-projects/')

    def test_description_is_optional(self):
        role = Role.objects.get(id=1)
        self.assertTrue(role._meta.get_field('description').blank)

    def test_description_content(self):
        role = Role.objects.get(id=1)
        expected_description = 'Test Description'
        self.assertEqual(role.description, expected_description)

    def test_visible_defaults_to_true(self):
        role = Role.objects.get(id=1)
        self.assertTrue(role.visible)

    def test_image_sm_max_length(self):
        role = Role.objects.get(id=1)
        max_length = role._meta.get_field('image_sm').max_length
        self.assertEqual(max_length, 200)

    def test_image_md_max_length(self):
        role = Role.objects.get(id=1)
        max_length = role._meta.get_field('image_md').max_length
        self.assertEqual(max_length, 200)

    def test_image_lg_max_length(self):
        role = Role.objects.get(id=1)
        max_length = role._meta.get_field('image_lg').max_length
        self.assertEqual(max_length, 200)

    def test_str_method(self):
        role = Role.objects.get(id=1)
        expected_object_name = 'Test Role'
        self.assertEqual(str(role), expected_object_name)


class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # NOTE: I'm using the name 'test_client' instead of 'client' to avoid a naming conflict with
        # the 'client' property of Django's TestCase, which is an instance of django.test.Client.
        cls.test_client = PortfolioClient.objects.create(name='Test Client', slug='test-client')
        cls.industry = Industry.objects.create(name='Test Industry', slug='test-industry')
        cls.market = Market.objects.create(name='Test Market', slug='test-market')
        cls.mediatype = MediaType.objects.create(name='Test MediaType', slug='test-mediatype')
        cls.role = Role.objects.create(name='Test Role', slug='test-role')

    def setUp(self):
        self.project = Project.objects.create(name='Test Project', slug='test-project', client=self.test_client)
        self.project.industry.add(self.industry)
        self.project.market.add(self.market)
        self.project.mediatype.add(self.mediatype)
        self.project.role.add(self.role)

    def test_name_label(self):
        field_label = self.project._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        max_length = self.project._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        self.assertEqual(self.project.get_absolute_url(), '/portfolio/project-details/test-project/')

    def test_str_method(self):
        self.assertEqual(str(self.project), 'Test Project')

    def test_get_verbose_name(self):
        self.assertEqual(self.project.get_verbose_name(), 'Project')

    def test_get_verbose_name_plural(self):
        self.assertEqual(self.project.get_verbose_name_plural(), 'Projects')

    def test_client_label(self):
        field_label = self.project._meta.get_field('client').verbose_name
        self.assertEqual(field_label, 'client')

    def test_client_is_assigned(self):
        self.assertEqual(self.project.client.name, 'Test Client')

    def test_industry_is_assigned(self):
        self.assertEqual(self.project.industry.first().name, 'Test Industry')

    def test_market_is_assigned(self):
        self.assertEqual(self.project.market.first().name, 'Test Market')

    def test_mediatype_is_assigned(self):
        self.assertEqual(self.project.mediatype.first().name, 'Test MediaType')

    def test_role_is_assigned(self):
        self.assertEqual(self.project.role.first().name, 'Test Role')


class ProjectItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.project = Project.objects.create(name='Test Project', slug='test-project')

    def setUp(self):
        # Set up for each individual test method
        self.project_item = ProjectItem.objects.create(name='Test ProjectItem', slug='test-projectitem', project=self.project)

    def test_name_label(self):
        field_label = self.project_item._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        max_length = self.project_item._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        self.assertEqual(self.project_item.get_absolute_url(), '/portfolio/project-details/test-projectitem/')

    def test_str_method(self):
        self.assertEqual(str(self.project_item), 'Test ProjectItem')

    def test_get_verbose_name(self):
        self.assertEqual(self.project_item.get_verbose_name(), 'Project Item')

    def test_get_verbose_name_plural(self):
        self.assertEqual(self.project_item.get_verbose_name_plural(), 'Project Items')

    def test_status_label(self):
        field_label = self.project_item._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_status_max_length(self):
        max_length = self.project_item._meta.get_field('status').max_length
        self.assertEqual(max_length, 2)

    def test_status_defaults_to_draft(self):
        self.assertEqual(self.project_item.status, 'D')

    def test_description_is_optional(self):
        self.assertTrue(self.project_item._meta.get_field('description').blank)

    def test_html_content_is_optional(self):
        self.assertTrue(self.project_item._meta.get_field('html_content').blank)

    def test_visible_defaults_to_true(self):
        self.assertTrue(self.project_item.visible)

    def test_item_order_is_optional(self):
        self.assertTrue(self.project_item._meta.get_field('item_order').blank)


class ProjectItemImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        project = Project.objects.create(name='Test Project', slug='test-project')
        project_item = ProjectItem.objects.create(name='Test ProjectItem', slug='test-projectitem', project=project)
        ProjectItemImage.objects.create(project_item=project_item, original='image.jpg', thumbnail='thumbnail.jpg', medium='medium.jpg', admin_list_thumb='admin_list_thumb.jpg')

    def test_original_max_length(self):
        projectitemimage = ProjectItemImage.objects.get(id=1)
        max_length = projectitemimage._meta.get_field('original').max_length
        self.assertEqual(max_length, 200)

    def test_thumbnail_max_length(self):
        projectitemimage = ProjectItemImage.objects.get(id=1)
        max_length = projectitemimage._meta.get_field('thumbnail').max_length
        self.assertEqual(max_length, 200)

    def test_medium_max_length(self):
        projectitemimage = ProjectItemImage.objects.get(id=1)
        max_length = projectitemimage._meta.get_field('medium').max_length
        self.assertEqual(max_length, 200)

    def test_medium_large_is_optional(self):
        projectitemimage = ProjectItemImage.objects.get(id=1)
        self.assertTrue(projectitemimage._meta.get_field('medium_large').blank)

    def test_large_is_optional(self):
        projectitemimage = ProjectItemImage.objects.get(id=1)
        self.assertTrue(projectitemimage._meta.get_field('large').blank)

    def test_admin_list_thumb_max_length(self):
        projectitemimage = ProjectItemImage.objects.get(id=1)
        max_length = projectitemimage._meta.get_field('admin_list_thumb').max_length
        self.assertEqual(max_length, 200)


class ProjectItemAttachmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        project = Project.objects.create(name='Test Project', slug='test-project')
        project_item = ProjectItem.objects.create(name='Test ProjectItem', slug='test-projectitem', project=project)
        ProjectItemAttachment.objects.create(project_item=project_item, file='file.pdf', link_text='Download')

    def test_link_text_max_length(self):
        projectitemattachment = ProjectItemAttachment.objects.get(id=1)
        max_length = projectitemattachment._meta.get_field('link_text').max_length
        self.assertEqual(max_length, 200)

    def test_str_method(self):
        projectitemattachment = ProjectItemAttachment.objects.get(id=1)
        self.assertEqual(str(projectitemattachment), 'file.pdf')

    def test_description_is_optional(self):
        projectitemattachment = ProjectItemAttachment.objects.get(id=1)
        self.assertTrue(projectitemattachment._meta.get_field('description').blank)

    def test_visible_defaults_to_true(self):
        projectitemattachment = ProjectItemAttachment.objects.get(id=1)
        self.assertTrue(projectitemattachment.visible)
