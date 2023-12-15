from django.shortcuts import render
from django.views import generic
from .models import Client, Industry, Market, MediaType, ProjectItem, Role, Project


def home(request):
    return render(request, 'pages/home/page.html')


def portfolio(request):
    return render(request, 'pages/portfolio/page.html')


def about(request):
    return render(request, 'pages/about/page.html')


def contact(request):
    return render(request, 'pages/contact/page.html')


def clients(request):
    clients = Client.objects.all()
    return render(request, 'pages/portfolio/clients/page.html', {'clients': clients, 'object': Client()})


class ClientProjectsListView(generic.DetailView):
    model = Client
    template_name = 'pages/portfolio/lists/client_projects_list.html'


def industries(request):
    industries = Industry.objects.all()
    return render(request, 'pages/portfolio/industries/page.html', {'industries': industries, 'object': Industry()})


class IndustryProjectsListView(generic.DetailView):
    model = Industry
    template_name = 'pages/portfolio/lists/industry_projects_list.html'


def markets(request):
    markets = Market.objects.all()
    return render(request, 'pages/portfolio/markets/page.html', {'markets': markets, 'object': Market()})


class MarketProjectsListView(generic.DetailView):
    model = Market
    template_name = 'pages/portfolio/lists/market_projects_list.html'


def mediatypes(request):
    mediatypes = MediaType.objects.all()
    return render(request, 'pages/portfolio/media_types/page.html', {'mediatypes': mediatypes, 'object': MediaType()})


class MediaTypeProjectsListView(generic.DetailView):
    model = MediaType
    template_name = 'pages/portfolio/lists/media_type_projects_list.html'


def roles(request):
    roles = Role.objects.all()
    return render(request, 'pages/portfolio/roles/page.html', {'roles': roles, 'object': Role()})


class RoleProjectsListView(generic.DetailView):
    model = Role
    template_name = 'pages/portfolio/lists/role_projects_list.html'


def projects(request):
    projects = Project.objects.all()
    return render(request, 'pages/portfolio/projects/page.html', {'projects': projects})


class ProjectItemsView(generic.DetailView):
    model = Project
    template_name = 'pages/portfolio/projects/project_items.html'


class ProjectDetailsView(generic.DetailView):
    model = Project
    template_name = 'pages/portfolio/projects/project_details.html'
