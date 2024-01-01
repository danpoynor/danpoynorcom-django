from .models import Project, ProjectItem, Client, Industry, Market, MediaType, Role
from .utils import get_visible_objects


def project_counts(request):
    global_total_projects = get_visible_objects(Project).count()
    global_total_project_items = get_visible_objects(ProjectItem).count()
    total_projects = get_visible_objects(Project).count()
    total_project_items = get_visible_objects(ProjectItem).count()
    total_clients = get_visible_objects(Client).count()
    total_industries = get_visible_objects(Industry).count()
    total_markets = get_visible_objects(Market).count()
    total_media_types = get_visible_objects(MediaType).count()
    total_roles = get_visible_objects(Role).count()

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
