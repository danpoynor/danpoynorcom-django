import re
from bakery.views import BuildableDetailView, BuildableTemplateView, BuildableListView
import inflect
from django.shortcuts import redirect
from django.db.models.functions import Lower
from django.db.models import OuterRef, Exists
from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem
from .mixins import PaginationMixin, PrevNextMixin, ProjectDetailsPrevNextMixin
from .utils import get_visible_objects
from .constants import SELECTED_CLIENT_IDS, SELECTED_INDUSTRY_IDS, SELECTED_MEDIA_TYPE_IDS, SELECTED_ROLE_IDS, HIGHLIGHTED_INDUSTRY_IDS, HIGHLIGHTED_MEDIA_TYPE_IDS, HIGHLIGHTED_ROLE_IDS

default_page_description = "Dan Poynor is a UI/UX designer and web developer in Austin, TX. He has worked with clients in a wide range of industries and markets, including startups, small businesses, and global brands."


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
    template_name = "portfolio/home.html"
    build_path = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dan Poynor : Visual / UX / Web Design & Development : Austin, TX'
        context['description'] = "UX/UI + ⚡️ Code: I solve business problems with creative strategy & technical expertise. I don't just make it pretty, I make it work."
        return context


class PortfolioView(BuildableTemplateView):
    template_name = "portfolio/portfolio.html"
    build_path = 'portfolio/index.html'

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
            "title": "Strategic Design + Dev Solutions for Every Industry & Medium",
            "description": "From Fortune 500s to startups, I've crafted award-winning UX/UI & web solutions across industries. Ready to unleash your brand's potential? ✨",
        })

        return context


class AboutView(BuildableTemplateView):
    template_name = "portfolio/about.html"
    build_path = 'about/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dan Poynor : UI/UX Design & Web Development : Austin, TX'
        context['description'] = "Meet your new design secret weapon! Quick-witted, multi-talented UX/UI design and development wiz with a proven track record of slaying digital dragons for diverse clients, big & small. Ready to unleash your brand's full potential? Let's chat."
        return context


class ContactView(BuildableTemplateView):
    template_name = "portfolio/contact.html"
    build_path = 'contact/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Let’s Connect! : UI/UX Design & Web Development : Austin, TX'
        context['description'] = "Don't be shy, partner! I'm just a click, call, or email away. Let's discuss how my design alchemy can transform your business. Send me your wildest ideas, and watch them become reality. ✨"
        return context


class ClientsView(BuildableTemplateView):
    template_name = "portfolio/client_list.html"
    build_path = 'portfolio/clients/index.html'

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
            "title": "Startups to Global Brands : Checkout My Design & Dev Clients",
            "description": "From silicon giants to indie darlings, I've powered success for diverse clients. Explore my global portfolio & find your perfect design partner.",
        })

        return context


class ClientProjectsListView(PaginationMixin, PrevNextMixin, BuildableDetailView):
    model = Client
    template_name = "portfolio/client_detail.html"
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

        context['title'] = f'{client_name} : Design & Dev Projects : Austin, TX : Page {page} {order_text}'
        context['description'] = f'Explore design and development projects for {client_name}. Page {page} {order_text}.'
        return context


class IndustriesView(BuildableTemplateView):
    template_name = "portfolio/industry_list.html"
    build_path = 'portfolio/industries/index.html'

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
            "title": "Making a Mark in Every Market: My Design & Dev Industry List",
            "description": "B2B, B2C, entertainment, non-profit? Conquered them all. Explore my industry expertise & unlock your brand's full potential.",
        })

        return context


class IndustryProjectsListView(PaginationMixin, PrevNextMixin, BuildableDetailView):
    model = Industry
    template_name = "portfolio/industry_detail.html"
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

        context['title'] = f'{industry_name} : Design & Dev Projects : Austin, TX : Page {page} {order_text}'
        context['description'] = f'Explore design and development projects for {industry_name}. Page {page} {order_text}.'
        return context


class MarketsView(BuildableTemplateView):
    template_name = "portfolio/market_list.html"
    build_path = 'portfolio/markets/index.html'

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
            "title": "Market-Driven Design & Development: View Tailored Solutions",
            "description": "From niche audiences to global markets, view my award-winning UX/UI & web solutions that speak their language. Built for success and maximum impact.",
        })

        return context


class MarketProjectsListView(PaginationMixin, PrevNextMixin, BuildableDetailView):
    model = Market
    template_name = "portfolio/market_detail.html"
    count_type = "market items"
    view_name = "market_page_order"
    filter_field = "market"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add the title to the context
        context['title'] = f'{self.object.name} Design & Development Expertise :  Austin, TX'
        context['description'] = f'Explore design and development projects for {self.object.name}.'
        return context


class MediaTypesView(BuildableTemplateView):
    template_name = "portfolio/mediatype_list.html"
    build_path = 'contact/index.html''portfolio/media_types/index.html'

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
            "title": "Pixels to Print & Beyond : View Engaging Design & Dev Mastery",
            "description": "From print to interactive, design with seamless flexibility. Discover my media expertise & let's craft experiences that captivate.",
        })

        return context


class MediaTypeProjectsListView(PaginationMixin, PrevNextMixin, BuildableDetailView):
    model = MediaType
    template_name = "portfolio/mediatype_detail.html"
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
            context['title'] = f'{singular_name} Portfolio : Austin, TX : Page {page} {order_text}'
            context['description'] = f'Explore the {singular_name} portfolio. Page {page} {order_text}.'
        else:
            context['title'] = f'{singular_name} Designer Portfolio : Austin, TX : Page {page} {order_text}'
            context['description'] = f'Explore the {singular_name} designer portfolio. Page {page} {order_text}.'
        return context


class RolesView(BuildableTemplateView):
    template_name = "portfolio/role_list.html"
    build_path = 'portfolio/roles/index.html'

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
            "title": "Concept to Creation: View My Diverse Design & Dev Experience",
            "description": "Concept to code, I wear many hats. Explore my multi-faceted skillset & find the perfect design partner for your project.",
        })

        return context


class RoleProjectsListView(PaginationMixin, PrevNextMixin, BuildableDetailView):
    model = Role
    template_name = "portfolio/role_detail.html"
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

        context['title'] = f'{role_name} Portfolio : Austin, TX : Page {page} {order_text}'
        context['description'] = f'Explore my {role_name} portfolio. Page {page} {order_text}.'
        return context


class ProjectsView(PaginationMixin, BuildableListView):
    template_name = "portfolio/project_list.html"
    view_name = "projects_page_order"
    paginator_template_name = "partials/pagination/_projects_paginator.html"
    model = Project
    build_path = 'portfolio/design-and-development-projects/index.html'

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
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

        return project_list

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
        title = f"Visual/UX/UI Design & Software Development Successes - Page {page} {order_text}"

        context.update({
            "page_obj": page_obj,
            "order": order,
            "pages": elided_page_range,
            "total_projects": total_projects,
            "count_type": "projects",  # Specify that we want to display the count of projects
            "view_name": self.view_name,  # The name of the current view
            "taxonomy_item_slug": "",  # There is no taxonomy item for this view
            "title": title,
            "description": default_page_description,
        })

        return context


class ProjectItemsView(PrevNextMixin, BuildableDetailView):
    model = Project
    template_name = "portfolio/project_items_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.object.items.filter(visible=True)
        context["title"] = f'Project Items: {self.object.name}'
        context['description'] = default_page_description
        return context


class ProjectDetailsView(ProjectDetailsPrevNextMixin, BuildableDetailView):
    model = ProjectItem
    template_name = "portfolio/project_details.html"

    def get_class_name(self):
        return self.__class__.__name__

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object.project
        context["items"] = project.get_ordered_items().filter(visible=True, project__visible=True)

        # Check if project item name and project name are the same
        if self.object.name == project.name:
            context['title'] = f'Project: {self.object.name}'
            context['description'] = f'Details about the project: {self.object.name}'
        else:
            context['title'] = f'Project: {project.name} : {self.object.name}'
            context['description'] = f'Details about the project: {project.name} and item: {self.object.name}'

        return context
