from django.db.models import Q
from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem


def get_visible_objects(model, role=None):
    # Define a Q object for the visible filter
    visible_filter = Q(visible=True)

    # Add conditions to the filter for each related model
    if issubclass(model, Client):
        visible_filter &= Q(project__visible=True, project__item__visible=True)
    elif issubclass(model, Industry):
        visible_filter &= Q(project__visible=True, project__item__visible=True, project__client__visible=True)
    elif issubclass(model, Market):
        visible_filter &= Q(project__visible=True, project__item__visible=True, project__client__visible=True)
    elif issubclass(model, MediaType):
        visible_filter &= Q(project__visible=True, project__item__visible=True, project__client__visible=True)
    elif issubclass(model, Role):
        visible_filter &= Q(project__visible=True, project__item__visible=True, project__client__visible=True)
    elif issubclass(model, Project):
        visible_filter &= Q(item__visible=True, client__visible=True, industry__visible=True, market__visible=True, mediatype__visible=True, role__visible=True)
    elif issubclass(model, ProjectItem):
        visible_filter &= Q(project__visible=True, project__client__visible=True)
        if role:
            visible_filter &= Q(project__role=role, project__role__visible=True)

    # Return the queryset of distinct visible objects
    queryset = model.objects.filter(visible_filter).distinct()

    # Exclude ProjectItem instances where the related Project has any Role that is not visible
    if issubclass(model, ProjectItem):
        queryset = queryset.exclude(project__role__visible=False)

    return queryset
