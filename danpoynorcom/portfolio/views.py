from django.shortcuts import render
from django.views import generic
from django.db.models.functions import Lower
from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem
from .mixins import PrevNextMixin


def home(request):
    return render(request, 'pages/home/page.html')


def portfolio(request):
    selected_client_ids = [42, 65, 4, 83, 37]
    selected_clients = Client.objects.filter(id__in=selected_client_ids)

    selected_industry_ids = [14, 32, 8, 3, 21]
    selected_industries = Industry.objects.filter(id__in=selected_industry_ids)

    selected_media_type_ids = [28, 3, 21, 36, 38]
    selected_media_types = MediaType.objects.filter(
        id__in=selected_media_type_ids)

    selected_role_ids = [12, 24, 22, 2, 8]
    selected_roles = Role.objects.filter(id__in=selected_role_ids)

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


def clients(request):
    clients = Client.objects.all().order_by(Lower('name'))
    return render(request, 'pages/portfolio/clients/page.html', {'clients': clients, 'object': Client()})


class ClientProjectsListView(PrevNextMixin, generic.DetailView):
    model = Client
    template_name = 'pages/portfolio/clients/projects_list_page.html'


def industries(request):
    highlighted_industry_ids = [3, 13, 32, 8, 21, 24]
    highlighted_industries = Industry.objects.filter(
        id__in=highlighted_industry_ids)
    industries = Industry.objects.all()

    context = {
        'highlighted_industries': highlighted_industries,
        'industries': industries,
        'object': Industry(),
    }

    return render(request, 'pages/portfolio/industries/page.html', context)


class IndustryProjectsListView(PrevNextMixin, generic.DetailView):
    model = Industry
    template_name = 'pages/portfolio/industries/projects_list_page.html'


def markets(request):
    markets = Market.objects.all()
    return render(request, 'pages/portfolio/markets/page.html', {'markets': markets, 'object': Market()})


class MarketProjectsListView(PrevNextMixin, generic.DetailView):
    model = Market
    template_name = 'pages/portfolio/markets/projects_list_page.html'


def mediatypes(request):
    highlighted_media_type_ids = [28, 3, 21, 36, 38]
    highlighted_media_types = MediaType.objects.filter(
        id__in=highlighted_media_type_ids)
    mediatypes = MediaType.objects.all()

    context = {
        'highlighted_media_types': highlighted_media_types,
        'mediatypes': mediatypes,
        'object': MediaType()
    }

    mediatypes = MediaType.objects.all()
    return render(request, 'pages/portfolio/media_types/page.html', context)


class MediaTypeProjectsListView(PrevNextMixin, generic.DetailView):
    model = MediaType
    template_name = 'pages/portfolio/media_types/projects_list_page.html'


def roles(request):
    highlighted_role_ids = [12, 24, 22, 2, 8]
    highlighted_roles = Role.objects.filter(id__in=highlighted_role_ids)
    roles = Role.objects.all()

    context = {
        'highlighted_roles': highlighted_roles,
        'roles': roles,
        'object': Role()
    }

    return render(request, 'pages/portfolio/roles/page.html', context)


class RoleProjectsListView(PrevNextMixin, generic.DetailView):
    model = Role
    template_name = 'pages/portfolio/roles/projects_list_page.html'


def projects(request):
    projects = Project.objects.all()
    return render(request, 'pages/portfolio/projects/page.html', {'projects': projects})


class ProjectItemsView(generic.DetailView):
    model = Project
    template_name = 'pages/portfolio/projects/project_items.html'


class ProjectDetailsView(generic.DetailView):
    model = ProjectItem
    template_name = 'pages/portfolio/projects/project_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object.project
        context['items'] = project.get_ordered_items()
        return context
