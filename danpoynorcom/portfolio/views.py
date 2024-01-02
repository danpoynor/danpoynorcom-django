from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import TemplateView
from django.db.models.functions import Lower
from django.db.models import OuterRef, Exists
from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem
from .mixins import PaginationMixin, PrevNextMixin, ProjectDetailsPrevNextMixin
from .utils import get_visible_objects
from .constants import SELECTED_CLIENT_IDS, SELECTED_INDUSTRY_IDS, SELECTED_MEDIA_TYPE_IDS, SELECTED_ROLE_IDS, HIGHLIGHTED_INDUSTRY_IDS, HIGHLIGHTED_MEDIA_TYPE_IDS, HIGHLIGHTED_ROLE_IDS


def get_taxonomy_objects_with_visible_projects(TaxonomyModel):
    # Subquery to check if a taxonomy object has any visible projects with visible items
    has_visible_projects_with_visible_items_subquery = Project.objects.filter(
        **{TaxonomyModel._meta.model_name: OuterRef("pk")},
        visible=True,
        item__visible=True  # Check for visible items
    )

    # Get taxonomy objects that have any visible projects with visible items
    taxonomy_objects = TaxonomyModel.objects.filter(visible=True).annotate(
        has_visible_projects_with_visible_items=Exists(has_visible_projects_with_visible_items_subquery)
    ).filter(has_visible_projects_with_visible_items=True)

    return taxonomy_objects


def home(request):
    return render(request, "pages/home/page.html")


def portfolio(request):
    selected_clients = Client.objects.filter(id__in=SELECTED_CLIENT_IDS)
    for client in selected_clients:
        visible_project_items = ProjectItem.objects.filter(
            project__client=client,
            project__visible=True,
            visible=True
        )
        client.project_item_count = visible_project_items.count()

    selected_industries = Industry.objects.filter(id__in=SELECTED_INDUSTRY_IDS)
    for industry in selected_industries:
        visible_project_items = ProjectItem.objects.filter(
            project__industry=industry,
            project__visible=True,
            visible=True
        )
        industry.project_item_count = visible_project_items.count()

    selected_media_types = MediaType.objects.filter(id__in=SELECTED_MEDIA_TYPE_IDS)
    for mediatype in selected_media_types:
        visible_project_items = ProjectItem.objects.filter(
            project__mediatype=mediatype,
            project__visible=True,
            visible=True
        )
        mediatype.project_item_count = visible_project_items.count()

    selected_roles = Role.objects.filter(id__in=SELECTED_ROLE_IDS)
    for role in selected_roles:
        visible_project_items = ProjectItem.objects.filter(
            project__role=role,
            project__visible=True,
            visible=True
        )
        role.project_item_count = visible_project_items.count()

    context = {
        "selected_clients": selected_clients,
        "selected_industries": selected_industries,
        "selected_media_types": selected_media_types,
        "selected_roles": selected_roles,
    }

    return render(request, "pages/portfolio/page.html", context)


def about(request):
    return render(request, "pages/about/page.html")


def contact(request):
    return render(request, "pages/contact/page.html")


def clients(request):
    client_list = get_visible_objects(Client).order_by(Lower("name"))
    for client in client_list:
        # Get visible projects for the current client
        visible_projects = get_visible_objects(Project).filter(client=client)

        # Get visible items for the visible projects
        visible_project_items = get_visible_objects(ProjectItem).filter(project__in=visible_projects)

        client.project_item_count = visible_project_items.count()

    return render(request, "pages/portfolio/clients/page.html", {"clients": client_list, "object": Client()})


class ClientProjectsListView(PaginationMixin, PrevNextMixin, generic.DetailView):
    model = Client
    template_name = "pages/portfolio/clients/term_items_page.html"
    count_type = "client items"
    view_name = "client_page_order"
    filter_field = "client"
    paginator_template_name = "partials/pagination/_paginator.html"


def industries(request):
    highlighted_industries = get_visible_objects(Industry).filter(id__in=HIGHLIGHTED_INDUSTRY_IDS)
    for industry in highlighted_industries:
        visible_project_items = ProjectItem.objects.filter(
            project__industry=industry,
            project__visible=True,
            visible=True
        )
        industry.project_item_count = visible_project_items.count()

    industry_list = get_visible_objects(Industry)
    for industry in industry_list:
        visible_project_items = ProjectItem.objects.filter(
            project__industry=industry,
            project__visible=True,
            visible=True
        )
        industry.project_item_count = visible_project_items.count()

    market_list = get_visible_objects(Market)
    for market in market_list:
        visible_project_items = ProjectItem.objects.filter(
            project__market=market,
            project__visible=True,
            visible=True
        )
        market.project_item_count = visible_project_items.count()

    context = {
        "highlighted_industries": highlighted_industries,
        "industries": industry_list,
        "markets": market_list,
        "object": Industry(),
    }

    return render(request, "pages/portfolio/industries/page.html", context)


class IndustryProjectsListView(PaginationMixin, PrevNextMixin, generic.DetailView):
    model = Industry
    template_name = "pages/portfolio/industries/term_items_page.html"
    count_type = "industry items"
    view_name = "industry_page_order"
    filter_field = "industry"
    paginator_template_name = "partials/pagination/_paginator.html"


def markets(request):
    market_list = get_taxonomy_objects_with_visible_projects(Market)
    for market in market_list:
        # Get visible projects for the current market
        visible_projects = get_visible_objects(Project).filter(market=market)

        # Get visible items for the visible projects
        visible_project_items = get_visible_objects(ProjectItem).filter(project__in=visible_projects)

        market.project_item_count = visible_project_items.count()

    return render(request, "pages/portfolio/markets/page.html", {"markets": market_list, "object": Market()})


class MarketProjectsListView(PaginationMixin, PrevNextMixin, generic.DetailView):
    model = Market
    template_name = "pages/portfolio/markets/term_items_page.html"
    count_type = "market items"
    view_name = "market_page_order"
    filter_field = "market"
    paginator_template_name = "partials/pagination/_paginator.html"


def mediatypes(request):
    highlighted_media_types = get_visible_objects(MediaType).filter(id__in=HIGHLIGHTED_MEDIA_TYPE_IDS)
    for mediatype in highlighted_media_types:
        visible_project_items = ProjectItem.objects.filter(
            project__mediatype=mediatype,
            project__visible=True,
            visible=True
        )
        mediatype.project_item_count = visible_project_items.count()

    mediatype_list = get_visible_objects(MediaType)
    for mediatype in mediatype_list:
        visible_project_items = ProjectItem.objects.filter(
            project__mediatype=mediatype,
            project__visible=True,
            visible=True
        )
        mediatype.project_item_count = visible_project_items.count()

    context = {
        "highlighted_media_types": highlighted_media_types,
        "mediatypes": mediatype_list,
        "object": MediaType()
    }

    return render(request, "pages/portfolio/media_types/page.html", context)


class MediaTypeProjectsListView(PaginationMixin, PrevNextMixin, generic.DetailView):
    model = MediaType
    template_name = "pages/portfolio/media_types/term_items_page.html"
    count_type = "media type items"
    view_name = "mediatype_page_order"
    filter_field = "mediatype"
    paginator_template_name = "partials/pagination/_paginator.html"


def roles(request):
    highlighted_roles = get_visible_objects(Role).filter(id__in=HIGHLIGHTED_ROLE_IDS)
    for role in highlighted_roles:
        visible_project_items = ProjectItem.objects.filter(
            project__role=role,
            project__visible=True,
            visible=True
        )
        role.project_item_count = visible_project_items.count()

    role_list = get_visible_objects(Role)
    for role in role_list:
        visible_project_items = get_visible_objects(ProjectItem, role)
        role.project_item_count = len(visible_project_items)

    context = {
        "highlighted_roles": highlighted_roles,
        "roles": role_list,
        "object": Role()
    }

    return render(request, "pages/portfolio/roles/page.html", context)


class RoleProjectsListView(PaginationMixin, PrevNextMixin, generic.DetailView):
    model = Role
    template_name = "pages/portfolio/roles/term_items_page.html"
    count_type = "role items"
    view_name = "role_page_order"
    filter_field = "role"
    paginator_template_name = "partials/pagination/_paginator.html"


class ProjectsView(PaginationMixin, TemplateView):
    template_name = "pages/portfolio/projects/page.html"
    view_name = "projects_page_order"
    paginator_template_name = "partials/pagination/_projects_paginator.html"

    def post(self, request, *args, **kwargs):
        # Get the selected order from the POST data
        order = request.POST.get("order", "asc")

        # Redirect to the first page with the selected order
        return redirect(self.view_name, page=1, order=order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Subquery to check if a project has any visible items
        has_visible_items_subquery = ProjectItem.objects.filter(
            project=OuterRef("pk"),
            visible=True  # Check for visible items
        )

        # Get projects that have any visible items
        project_list = Project.objects.filter(
            visible=True
        ).annotate(
            has_visible_items=Exists(has_visible_items_subquery)
        ).filter(
            has_visible_items=True
        )

        # Get the page number from the URL
        page = self.kwargs.get("page")

        # Get the order from the URL, default to 'asc' if not provided
        order = self.kwargs.get("order", "asc")

        # Paginate items
        page_obj, order, elided_page_range, total_projects = self.paginate_queryset(project_list, page, order)

        context.update({
            "page_obj": page_obj,
            "order": order,
            "pages": elided_page_range,
            "total_projects": total_projects,
            "count_type": "projects",  # Specify that we want to display the count of projects
            "view_name": self.view_name,  # The name of the current view
            "taxonomy_item_slug": "",  # There is no taxonomy item for this view
        })

        return context


class ProjectItemsView(PrevNextMixin, generic.DetailView):
    model = Project
    template_name = "pages/portfolio/projects/project_items.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.object.items.filter(visible=True)
        return context


class ProjectDetailsView(ProjectDetailsPrevNextMixin, generic.DetailView):
    model = ProjectItem
    template_name = "pages/portfolio/projects/project_details.html"

    def get_class_name(self):
        return self.__class__.__name__

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object.project
        context["items"] = project.get_ordered_items().filter(visible=True, project__visible=True)
        return context
