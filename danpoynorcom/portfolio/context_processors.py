from .models import Project, ProjectItem, Client, Industry, Market, MediaType, Role


def project_counts(request):
    global_total_projects = Project.visible_objects.count()
    global_total_project_items = ProjectItem.visible_objects.count()
    total_projects = Project.visible_objects.count()
    total_project_items = ProjectItem.visible_objects.count()
    total_clients = Client.visible_objects.count()
    total_industries = Industry.visible_objects.count()
    total_markets = Market.visible_objects.count()
    total_media_types = MediaType.visible_objects.count()
    total_roles = Role.visible_objects.count()

    return {
        'global_total_projects': global_total_projects,
        'global_total_project_items': global_total_project_items,
        'total_projects': total_projects,
        'total_project_items': total_project_items,
        'total_clients': total_clients,
        'total_industries': total_industries,
        'total_markets': total_markets,
        'total_media_types': total_media_types,
        'total_roles': total_roles,
    }
