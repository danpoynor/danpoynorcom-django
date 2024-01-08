from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem


class ClientSitemap(Sitemap):
    def items(self):
        # Include a None item for the list of clients
        return list(Client.objects.all()) + [None]

    def location(self, item):
        if item is None:
            # Return the URL for the list of clients
            return reverse('clients')

        # Return the URL for the client detail page
        return reverse('client_detail', args=[item.slug])


class IndustrySitemap(Sitemap):
    def items(self):
        # Include a None item for the list of industries
        return list(Industry.objects.all()) + [None]

    def location(self, item):
        if item is None:
            # Return the URL for the list of industries
            return reverse('industries')

        # Return the URL for the industry detail page
        return reverse('industry_detail', args=[item.slug])


class MarketSitemap(Sitemap):
    def items(self):
        # Include a None item for the list of markets
        return list(Market.objects.all()) + [None]

    def location(self, item):
        if item is None:
            # Return the URL for the list of markets
            return reverse('markets')

        # Return the URL for the mark detail page
        return reverse('market_detail', args=[item.slug])


class MediaTypeSitemap(Sitemap):
    def items(self):
        # Include a None item for the list of mediatypes
        return list(MediaType.objects.all()) + [None]

    def location(self, item):
        if item is None:
            # Return the URL for the list of mediatypes
            return reverse('mediatypes')

        # Return the URL for the client detail page
        return reverse('mediatype_detail', args=[item.slug])


class RoleSitemap(Sitemap):
    def items(self):
        # Include a None item for the list of clients
        return list(Role.objects.all()) + [None]

    def location(self, item):
        if item is None:
            # Return the URL for the list of roles
            return reverse('roles')

        # Return the URL for the role detail page
        return reverse('role_detail', args=[item.slug])


# TODO: Need to fix
class ProjectSitemap(Sitemap):
    def items(self):
        # Include a None item for the list of clients
        return list(Project.objects.all()) + [None]

    def location(self, item):
        if item is None:
            # Return the URL for the list of projects
            return reverse('projects')

        # Return the URL for the project detail page
        return reverse('project_detail', args=[item.slug])


# TODO
class ProjectItemSitemap(Sitemap):
    def items(self):
        return ProjectItem.objects.none()

    def location(self, item):
        return reverse('project_detail', args=[item.pk])


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'portfolio', 'about', 'contact']

    def location(self, item):
        return reverse(item)
