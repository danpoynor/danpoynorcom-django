from .models import Project, ProjectItem, Client, Industry, Market, MediaType, Role


def project_counts(request):
    total_projects = Project.objects.count()
    total_project_items = ProjectItem.objects.count()
    total_clients = Client.objects.count()
    total_industries = Industry.objects.count()
    total_markets = Market.objects.count()
    total_media_types = MediaType.objects.count()
    total_roles = Role.objects.count()

    return {
        'total_projects': total_projects,
        'total_project_items': total_project_items,
        'total_clients': total_clients,
        'total_industries': total_industries,
        'total_markets': total_markets,
        'total_media_types': total_media_types,
        'total_roles': total_roles,
    }
