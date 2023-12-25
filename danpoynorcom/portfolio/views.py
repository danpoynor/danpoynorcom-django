from django.shortcuts import render
from django.views import generic
from django.db.models.functions import Lower
from django.db.models import OuterRef, Exists
from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem
from .mixins import PrevNextMixin, ProjectDetailsPrevNextMixin
from .utils import get_visible_objects


def get_taxonomy_objects_with_visible_projects(TaxonomyModel):
    # Subquery to check if a taxonomy object has any visible projects with visible items
    has_visible_projects_with_visible_items_subquery = Project.objects.filter(
        **{TaxonomyModel._meta.model_name: OuterRef('pk')},
        visible=True,
        item__visible=True  # Check for visible items
    )

    # Get taxonomy objects that have any visible projects with visible items
    taxonomy_objects = TaxonomyModel.objects.filter(visible=True).annotate(
        has_visible_projects_with_visible_items=Exists(has_visible_projects_with_visible_items_subquery)
    ).filter(has_visible_projects_with_visible_items=True)

    return taxonomy_objects


def home(request):
    return render(request, 'pages/home/page.html')


def portfolio(request):
    selected_client_ids = [42, 65, 4, 83, 37]
    selected_clients = Client.objects.filter(id__in=selected_client_ids)
    for client in selected_clients:
        visible_project_items = ProjectItem.objects.filter(
            project__client=client,
            project__visible=True,
            visible=True
        )
        client.project_item_count = visible_project_items.count()

    selected_industry_ids = [14, 32, 8, 3, 21]
    selected_industries = Industry.objects.filter(id__in=selected_industry_ids)
    for industry in selected_industries:
        visible_project_items = ProjectItem.objects.filter(
            project__industry=industry,
            project__visible=True,
            visible=True
        )
        industry.project_item_count = visible_project_items.count()

    selected_media_type_ids = [28, 3, 21, 36, 38]
    selected_media_types = MediaType.objects.filter(id__in=selected_media_type_ids)
    for mediatype in selected_media_types:
        visible_project_items = ProjectItem.objects.filter(
            project__mediatype=mediatype,
            project__visible=True,
            visible=True
        )
        mediatype.project_item_count = visible_project_items.count()

    selected_role_ids = [12, 24, 22, 2, 8]
    selected_roles = Role.objects.filter(id__in=selected_role_ids)
    for role in selected_roles:
        visible_project_items = ProjectItem.objects.filter(
            project__role=role,
            project__visible=True,
            visible=True
        )
        role.project_item_count = visible_project_items.count()

    context = {
        'selected_clients': selected_clients,
        'selected_industries': selected_industries,
        'selected_media_types': selected_media_types,
        'selected_roles': selected_roles,
    }

    return render(request, 'pages/portfolio/page.html', context)


def about(request):
    return render(request, 'pages/about/page.html')


def contact(request):
    return render(request, 'pages/contact/page.html')


def getty_legal_notice(request):
    return render(request, 'pages/legal-notice-to-picscout-getty-images-picscout-clients-cyveillance-you-are-prohibited-from-accessing-this-site/page.html')


def clients(request):
    client_list = get_visible_objects(Client).order_by(Lower('name'))
    for client in client_list:
        visible_project_items = ProjectItem.objects.filter(
            project__client=client,
            project__visible=True,
            visible=True
        )
        client.project_item_count = visible_project_items.count()

    return render(request, 'pages/portfolio/clients/page.html', {'clients': client_list, 'object': Client()})


class ClientProjectsListView(PrevNextMixin, generic.DetailView):
    model = Client
    template_name = 'pages/portfolio/clients/term_items_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get visible projects for the current client
        visible_projects = get_visible_objects(Project).filter(client=self.object)

        # Get visible items for the visible projects
        context['all_items'] = get_visible_objects(ProjectItem).filter(project__in=visible_projects)

        return context


def industries(request):
    highlighted_industry_ids = [3, 13, 32, 8, 21, 24]
    highlighted_industries = get_visible_objects(Industry).filter(id__in=highlighted_industry_ids)
    for industry in highlighted_industries:
        visible_project_items = ProjectItem.objects.filter(
            project__industry=industry,
            project__visible=True,
            visible=True
        )
        industry.project_item_count = visible_project_items.count()

    industry_list = get_visible_objects(Industry)
    for industry in industry_list:
        visible_project_items = ProjectItem.objects.filter(
            project__industry=industry,
            project__visible=True,
            visible=True
        )
        industry.project_item_count = visible_project_items.count()

    market_list = get_visible_objects(Market)
    for market in market_list:
        visible_project_items = ProjectItem.objects.filter(
            project__market=market,
            project__visible=True,
            visible=True
        )
        market.project_item_count = visible_project_items.count()

    context = {
        'highlighted_industries': highlighted_industries,
        'industries': industry_list,
        'markets': market_list,
        'object': Industry(),
    }

    return render(request, 'pages/portfolio/industries/page.html', context)


class IndustryProjectsListView(PrevNextMixin, generic.DetailView):
    model = Industry
    template_name = 'pages/portfolio/industries/term_items_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_items'] = get_visible_objects(ProjectItem).filter(project__in=self.object.projects.all())
        return context


def markets(request):
    market_list = get_taxonomy_objects_with_visible_projects(Market)
    for market in market_list:
        visible_project_items = ProjectItem.objects.filter(
            project__market=market,
            project__visible=True,
            visible=True
        )
        market.project_item_count = visible_project_items.count()

    return render(request, 'pages/portfolio/markets/page.html', {'markets': market_list, 'object': Market()})


class MarketProjectsListView(PrevNextMixin, generic.DetailView):
    model = Market
    template_name = 'pages/portfolio/markets/term_items_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_items'] = ProjectItem.objects.filter(project__in=self.object.projects.filter(visible=True))
        return context


def mediatypes(request):
    highlighted_media_type_ids = [28, 3, 21, 36, 38]
    highlighted_media_types = get_visible_objects(MediaType).filter(id__in=highlighted_media_type_ids)
    for mediatype in highlighted_media_types:
        visible_project_items = ProjectItem.objects.filter(
            project__mediatype=mediatype,
            project__visible=True,
            visible=True
        )
        mediatype.project_item_count = visible_project_items.count()

    mediatype_list = get_visible_objects(MediaType)
    for mediatype in mediatype_list:
        visible_project_items = ProjectItem.objects.filter(
            project__mediatype=mediatype,
            project__visible=True,
            visible=True
        )
        mediatype.project_item_count = visible_project_items.count()

    context = {
        'highlighted_media_types': highlighted_media_types,
        'mediatypes': mediatype_list,
        'object': MediaType()
    }

    return render(request, 'pages/portfolio/media_types/page.html', context)


class MediaTypeProjectsListView(PrevNextMixin, generic.DetailView):
    model = MediaType
    template_name = 'pages/portfolio/media_types/term_items_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_items'] = get_visible_objects(ProjectItem).filter(project__in=self.object.projects.all())
        return context


def roles(request):
    highlighted_role_ids = [12, 24, 22, 2, 8]
    highlighted_roles = get_visible_objects(Role).filter(id__in=highlighted_role_ids)
    for role in highlighted_roles:
        visible_project_items = ProjectItem.objects.filter(
            project__role=role,
            project__visible=True,
            visible=True
        )
        role.project_item_count = visible_project_items.count()

    role_list = get_visible_objects(Role)
    for role in role_list:
        visible_project_items = get_visible_objects(ProjectItem, role)
        role.project_item_count = len(visible_project_items)

    context = {
        'highlighted_roles': highlighted_roles,
        'roles': role_list,
        'object': Role()
    }

    return render(request, 'pages/portfolio/roles/page.html', context)


class RoleProjectsListView(PrevNextMixin, generic.DetailView):
    model = Role
    template_name = 'pages/portfolio/roles/term_items_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_items'] = get_visible_objects(ProjectItem, self.object).filter(project__in=self.object.projects.all())
        return context


def projects(request):
    # Subquery to check if a project has any visible items
    has_visible_items_subquery = ProjectItem.objects.filter(
        project=OuterRef('pk'),
        visible=True  # Check for visible items
    )

    # Get projects that have any visible items
    project_list = Project.objects.filter(
        visible=True
    ).annotate(
        has_visible_items=Exists(has_visible_items_subquery)
    ).filter(
        has_visible_items=True
    )

    return render(request, 'pages/portfolio/projects/page.html', {'projects': project_list})


class ProjectItemsView(PrevNextMixin, generic.DetailView):
    model = Project
    template_name = 'pages/portfolio/projects/project_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.filter(visible=True)
        return context


class ProjectDetailsView(ProjectDetailsPrevNextMixin, generic.DetailView):
    model = ProjectItem
    template_name = 'pages/portfolio/projects/project_details.html'

    def get_class_name(self):
        return self.__class__.__name__

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object.project
        context['items'] = project.get_ordered_items().filter(visible=True, project__visible=True)
        return context
