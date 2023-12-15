from .models import Project, ProjectItem


def project_counts(request):
    total_projects = Project.objects.count()
    total_project_items = ProjectItem.objects.count()

    return {
        'total_projects': total_projects,
        'total_project_items': total_project_items,
    }
