from django.shortcuts import render
from django.views import generic
from .models import Client, Industry, Market, MediaType, Role, Project


def home(request):
    return render(request, 'index.html')


def portfolio(request):
    return render(request, 'portfolio.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def clients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients': clients})


class ClientDetailView(generic.DetailView):
    model = Client
    template_name = 'client_detail.html'


def industries(request):
    industries = Industry.objects.all()
    return render(request, 'industries.html', {'industries': industries})


class IndustryDetailView(generic.DetailView):
    model = Industry
    template_name = 'industry_detail.html'


def markets(request):
    markets = Market.objects.all()
    return render(request, 'markets.html', {'markets': markets})


class MarketDetailView(generic.DetailView):
    model = Market
    template_name = 'market_detail.html'


def mediatypes(request):
    mediatypes = MediaType.objects.all()
    return render(request, 'mediatypes.html', {'mediatypes': mediatypes})


class MediaTypeDetailView(generic.DetailView):
    model = MediaType
    template_name = 'mediatype_detail.html'


def roles(request):
    roles = Role.objects.all()
    return render(request, 'roles.html', {'roles': roles})


class RoleDetailView(generic.DetailView):
    model = Role
    template_name = 'role_detail.html'


def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})


class ProjectDetailsView(generic.DetailView):
    model = Project
    template_name = 'project_details.html'
