from bakery.views import BuildableTemplateView
import re
import inflect
from bakery.views import BuildableDetailView, BuildableTemplateView
from django.shortcuts import render, redirect
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


def capitalize_special_words(word):
    special_words = {
        "aol": "AOL",
        "specification": "Specifications",
        "html": "HTML",
        "pop": "POP",
        "video": "Video Editing",
        "ux": "UX",
        "cx": "CX",
        "ui": "UI",
        "uc": "UC",
        "hp": "HP",
        "fm": "FM",
        "fyi": "FYI",
        "vdo": "VDO",
        "adp": "ADP",
        "khn": "KHN",
        "ppc": "PPC",
        "rgb": "RGB",
        "kcea": "KCEA",
        "cnet": "CNET",
        "cort": "CORT",
        "imvu": "IMVU",
        "calarts": "CalArts",
        "calfinder": "CalFinder",
        "blufire": "BluFire",
        "tixnix": "TixNix",
        "singlefeed": "SingleFeed",
        "adbrite": "AdBrite",
        "bactrack": "BACtrack",
        "inetdvd": "iNetDVD",
        "jarmedia": "JarMedia",
        "echosign": "EchoSign",
        "workbright": "WorkBright",
        "businessuites": "BusinesSuites",
        "tacitlogic": "TacitLogic",
        "peoplesoft": "PeopleSoft",
        "myofferpal": "MyOfferPal",
        "grandmutual": "GrandMutual",
        "macphee": "MacPhee",
        "webex": "WebEx",
        "stellaservice": "StellaService",
        "quantbench": "QuantBench",
        "nextcustomer": "NextCustomer",
        "reallygreatrate": "ReallyGreatRate",
        "homerun.com": "HomeRun.com",
        "fiftyflowers.com": "FiftyFlowers.com"
    }
    return special_words.get(word.lower(), word)


class HomeView(BuildableTemplateView):
    template_name = "pages/home/page.html"
    build_path = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dan Poynor - Visual, UX, Web Design & Development | Austin, TX'
        return context


class PortfolioView(BuildableTemplateView):
    template_name = "pages/portfolio/page.html"
    build_path = 'portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

        context.update({
            "selected_clients": selected_clients,
            "selected_industries": selected_industries,
            "selected_media_types": selected_media_types,
            "selected_roles": selected_roles,
            "title": "Design + Dev Alchemy: Crafting Solutions for Every Industry & Medium",
        })

        return context


class AboutView(BuildableTemplateView):
    template_name = "pages/about/page.html"
    build_path = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Me'
        return context


class ContactView(BuildableTemplateView):
    template_name = "pages/contact/page.html"
    build_path = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Me'
        return context


class ClientsView(BuildableTemplateView):
    template_name = "pages/portfolio/clients/page.html"
    build_path = 'clients.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        client_list = get_visible_objects(Client).order_by(Lower("name"))
        for client in client_list:
            # Get visible projects for the current client
            visible_projects = get_visible_objects(Project).filter(client=client)

            # Get visible items for the visible projects
            visible_project_items = get_visible_objects(ProjectItem).filter(project__in=visible_projects)

            client.project_item_count = visible_project_items.count()

        context.update({
            "clients": client_list,
            "object": Client(),
            "title": "Startups to Global Brands: My Extensive Design & Development Client List",
        })

        return context


class ClientProjectsListView(PaginationMixin, PrevNextMixin, BuildableDetailView):
    model = Client
    template_name = "pages/portfolio/clients/term_items_page.html"
    count_type = "client items"
    view_name = "client_page_order"
    filter_field = "client"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add the title to the context
        client_name = self.object.name.title()
        words = re.split(r'(\s|/)', client_name)
        words = [capitalize_special_words(word) for word in words]
        client_name = "".join(words)
        # Check if ".Com" is in the name and replace it with ".com"
        if ".Com" in client_name:
            client_name = client_name.replace(".Com", ".com")

        # Get the page number and order from the request's query parameters
        page = self.kwargs.get('page', '1')
        order = self.kwargs.get('order', 'asc')
        order_text = "Asc" if order == "asc" else "Desc"

        context['title'] = f'{client_name} Design & Development Projects | Austin, Texas - Page {page} {order_text}'
        return context


class IndustriesView(BuildableTemplateView):
    template_name = "pages/portfolio/industries/page.html"
    build_path = 'industries.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

        context.update({
            "highlighted_industries": highlighted_industries,
            "industries": industry_list,
            "markets": market_list,
            "object": Industry(),
            "title": "Making a Mark in Every Market: My Design & Development Industry List",
        })

        return context


class IndustryProjectsListView(PaginationMixin, PrevNextMixin, BuildableDetailView):
    model = Industry
    template_name = "pages/portfolio/industries/term_items_page.html"
    count_type = "industry items"
    view_name = "industry_page_order"
    filter_field = "industry"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add the title to the context
        industry_name = self.object.name.title()
        words = re.split(r'(\s|/)', industry_name)
        words = [capitalize_special_words(word) for word in words]
        industry_name = "".join(words)
        # Check if "Projects" is already in the name
        if "Projects" in industry_name:
            industry_name = industry_name.replace("Projects", "").strip()

        # Get the page number and order from the request's query parameters
        page = self.kwargs.get('page', '1')
        order = self.kwargs.get('order', 'asc')
        order_text = "Asc" if order == "asc" else "Desc"

        context['title'] = f'{industry_name} Design Projects | Austin, Texas - Page {page} {order_text}'
        return context


class MarketsView(BuildableTemplateView):
    template_name = "pages/portfolio/markets/page.html"
    build_path = 'markets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        market_list = get_taxonomy_objects_with_visible_projects(Market)
        for market in market_list:
            # Get visible projects for the current market
            visible_projects = get_visible_objects(Project).filter(market=market)

            # Get visible items for the visible projects
            visible_project_items = get_visible_objects(ProjectItem).filter(project__in=visible_projects)

            market.project_item_count = visible_project_items.count()

        context.update({
            "markets": market_list,
            "object": Market(),
        })

        return context


class MarketProjectsListView(PaginationMixin, PrevNextMixin, BuildableDetailView):
    model = Market
    template_name = "pages/portfolio/markets/term_items_page.html"
    count_type = "market items"
    view_name = "market_page_order"
    filter_field = "market"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add the title to the context
        context['title'] = f'Portfolio Market: {self.object.name}'
        return context


class MediaTypesView(BuildableTemplateView):
    template_name = "pages/portfolio/media_types/page.html"
    build_path = 'media_types.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

        context.update({
            "highlighted_media_types": highlighted_media_types,
            "mediatypes": mediatype_list,
            "object": MediaType(),
            "title": "Pixels to Print & Beyond: Engaging Design & Development Mastery",
        })

        return context


class MediaTypeProjectsListView(PaginationMixin, PrevNextMixin, BuildableDetailView):
    model = MediaType
    template_name = "pages/portfolio/media_types/term_items_page.html"
    count_type = "media type items"
    view_name = "mediatype_page_order"
    filter_field = "mediatype"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Create an engine
        p = inflect.engine()
        # Try to convert plural to singular
        singular_name = p.singular_noun(self.object.name)
        # If singular_noun returned False, use the original name
        if not singular_name:
            singular_name = self.object.name
        else:
            # Capitalize the first letter of each word
            singular_name = singular_name.title()
        # Replace "Displays" with "Display"
        singular_name = singular_name.replace("Displays", "Display")
        # Replace words
        words = singular_name.split()
        words = [capitalize_special_words(word) for word in words]
        singular_name = " ".join(words)

        # Get the page number and order from the URL path parameters
        page = self.kwargs.get('page', '1')
        order = self.kwargs.get('order', 'asc')
        order_text = "Asc" if order == "asc" else "Desc"

        # Check if "Design" is already in the name
        if "Design" in singular_name or "Video Editing" in singular_name or "Photography" in singular_name:
            context['title'] = f'{singular_name} Portfolio | Austin, Texas - Page {page} {order_text}'
        else:
            context['title'] = f'{singular_name} Designer Portfolio | Austin, Texas - Page {page} {order_text}'
        return context


class RolesView(BuildableTemplateView):
    template_name = "pages/portfolio/roles/page.html"
    build_path = 'roles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

        context.update({
            "highlighted_roles": highlighted_roles,
            "roles": role_list,
            "object": Role(),
            "title": "Concept to Creation: My Diverse Design & Development Experience",
        })

        return context


class RoleProjectsListView(PaginationMixin, PrevNextMixin, BuildableDetailView):
    model = Role
    template_name = "pages/portfolio/roles/term_items_page.html"
    count_type = "role items"
    view_name = "role_page_order"
    filter_field = "role"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add the title to the context
        role_name = self.object.name.title()
        words = re.split(r'(\s|/)', role_name)
        words = [capitalize_special_words(word) for word in words]
        role_name = "".join(words)

        # Get the page number and order from the URL path parameters
        page = self.kwargs.get('page', '1')
        order = self.kwargs.get('order', 'asc')
        order_text = "Asc" if order == "asc" else "Desc"

        context['title'] = f'{role_name} Portfolio | Austin, Texas - Page {page} {order_text}'
        return context


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

        # Get the page number and order from the URL
        page = self.kwargs.get("page", '1')

        # Get the order from the URL, default to 'asc' if not provided
        order = self.kwargs.get("order", "asc")

        # Paginate items
        page_obj, order, elided_page_range, total_projects = self.paginate_queryset(project_list, page, order)

        # Create a title that includes the page number and order
        order_text = "Asc" if order == "asc" else "Desc"
        title = f"Design & Development Project Successes - Page {page} {order_text}"

        context.update({
            "page_obj": page_obj,
            "order": order,
            "pages": elided_page_range,
            "total_projects": total_projects,
            "count_type": "projects",  # Specify that we want to display the count of projects
            "view_name": self.view_name,  # The name of the current view
            "taxonomy_item_slug": "",  # There is no taxonomy item for this view
            "title": title,
        })

        return context


class ProjectItemsView(PrevNextMixin, BuildableDetailView):
    model = Project
    template_name = "pages/portfolio/projects/project_items.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.object.items.filter(visible=True)
        context["title"] = f'Project Items: {self.object.name}'
        return context


class ProjectDetailsView(ProjectDetailsPrevNextMixin, BuildableDetailView):
    model = ProjectItem
    template_name = "pages/portfolio/projects/project_details.html"

    def get_class_name(self):
        return self.__class__.__name__

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object.project
        context["items"] = project.get_ordered_items().filter(visible=True, project__visible=True)

        # Check if project item name and project name are the same
        if self.object.name == project.name:
            context['title'] = f'Project Detail: {self.object.name}'
        else:
            context['title'] = f'Project Detail: {project.name}: {self.object.name}'

        return context
