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
    selected_media_types = MediaType.objects.filter(id__in=selected_media_type_ids)

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
    client_list = Client.objects.all().order_by(Lower('name'))
    return render(request, 'pages/portfolio/clients/page.html', {'clients': client_list, 'object': Client()})


def getty_legal_notice(request):
    return render(request, 'pages/legal-notice-to-picscout-getty-images-picscout-clients-cyveillance-you-are-prohibited-from-accessing-this-site/page.html')


class ClientProjectsListView(PrevNextMixin, generic.DetailView):
    model = Client
    template_name = 'pages/portfolio/clients/term_items_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_items'] = ProjectItem.objects.filter(project__in=self.object.projects.all())
        return context


def industries(request):
    highlighted_industry_ids = [3, 13, 32, 8, 21, 24]
    highlighted_industries = Industry.objects.filter(id__in=highlighted_industry_ids)
    industry_list = Industry.objects.all()
    market_list = Market.objects.all()

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
        context['all_items'] = ProjectItem.objects.filter(project__in=self.object.projects.all())
        return context


def markets(request):
    market_list = Market.objects.all()
    return render(request, 'pages/portfolio/markets/page.html', {'markets': market_list, 'object': Market()})


class MarketProjectsListView(PrevNextMixin, generic.DetailView):
    model = Market
    template_name = 'pages/portfolio/markets/term_items_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_items'] = ProjectItem.objects.filter(project__in=self.object.projects.all())
        return context


def mediatypes(request):
    highlighted_media_type_ids = [28, 3, 21, 36, 38]
    highlighted_media_types = MediaType.objects.filter(id__in=highlighted_media_type_ids)
    mediatype_list = MediaType.objects.all()

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
        context['all_items'] = ProjectItem.objects.filter(project__in=self.object.projects.all())
        return context


def roles(request):
    highlighted_role_ids = [12, 24, 22, 2, 8]
    highlighted_roles = Role.objects.filter(id__in=highlighted_role_ids)
    role_list = Role.objects.all()

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
        context['all_items'] = ProjectItem.objects.filter(project__in=self.object.projects.all())
        return context


def projects(request):
    project_list = Project.objects.all()
    return render(request, 'pages/portfolio/projects/page.html', {'projects': project_list})


class ProjectItemsView(PrevNextMixin, generic.DetailView):
    model = Project
    template_name = 'pages/portfolio/projects/project_items.html'


class ProjectDetailsView(PrevNextMixin, generic.DetailView):
    model = ProjectItem
    template_name = 'pages/portfolio/projects/project_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object.project
        context['items'] = project.get_ordered_items()
        return context
