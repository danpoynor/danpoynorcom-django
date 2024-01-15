from os import path, stat
from datetime import datetime
import re
import json
import inflect
import requests
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models.functions import Lower
from django.db.models import OuterRef, Exists
from django.views.generic import TemplateView, DetailView, ListView
from .constants import PAGINATE_BY
from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem
from .mixins import PaginationMixin, PrevNextMixin, ProjectDetailsPrevNextMixin
from .utils import get_visible_objects
from .constants import SELECTED_CLIENT_IDS, SELECTED_INDUSTRY_IDS, SELECTED_MEDIA_TYPE_IDS, SELECTED_ROLE_IDS, HIGHLIGHTED_INDUSTRY_IDS, HIGHLIGHTED_MEDIA_TYPE_IDS, HIGHLIGHTED_ROLE_IDS

DEFAULT_PAGE_DESCRIPTION = "Dan Poynor is a UI/UX designer and web developer in Austin, TX. He has worked with clients in a wide range of industries and markets, including startups, small businesses, and global brands."


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


def website_seo_overview(request):
    # List of view names for the URLs
    view_names = ['home', 'portfolio', 'about', 'contact', 'client_list', 'industry_list', 'market_list', 'mediatype_list', 'role_list']

    # List of models for the URLs
    models = [Client, Industry, Market, MediaType, Role, Project, ProjectItem]

    # Build the list of URLs
    urls = [request.build_absolute_uri(reverse(view_name)) for view_name in view_names]
    for model in models:
        urls.extend(request.build_absolute_uri(obj.get_absolute_url()) for obj in model.objects.all())
    for client in Client.objects.all():
        urls.append(request.build_absolute_uri(client.get_absolute_url()))

    # Fetch and save the data when the refresh button is clicked
    if 'refresh_seo_data' in request.GET:
        seo_data = []
        for url in urls:
            # Try to get the data from the cache
            data = cache.get(f'seo_data_{url}')

            # If the data is not in the cache, fetch it from the web page
            if not data:
                try:
                    response = requests.get(url, timeout=5)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = str(soup.title.string) if soup.title else ''
                    description_tag = soup.find('meta', attrs={'name': 'description'})
                    description = str(description_tag['content']) if description_tag else ''
                    h1_tags = [str(tag.get_text(strip=True)) for tag in soup.find_all('h1')]
                    word_count = len(soup.get_text().split())
                    data = {
                        'url': url,
                        'title': title,
                        'description': description,
                        'h1_tags': h1_tags,
                        'word_count': word_count,
                    }
                    cache.set(f'seo_data_{url}', data, 3600)  # Cache the data for 1 hour
                except requests.exceptions.RequestException as e:
                    print(f'Error fetching {url}: {e}')
                    continue

            seo_data.append(data)

        # Save the data to a JSON file
        with open('portfolio/output/seo_data.json', 'w', encoding='utf-8') as f:
            json.dump(seo_data, f)

    # Load the data from the JSON file
    try:
        with open('portfolio/output/seo_data.json', 'r', encoding='utf-8') as f:
            seo_data = json.load(f)
    except FileNotFoundError:
        seo_data = []

    # Get the total number of items before filtering
    seo_data_total_length = len(seo_data)

    # Filter the data based on the search query
    search_query = request.GET.get('search_term', '')  # Default to empty string if not provided
    if search_query:
        seo_data = [item for item in seo_data if search_query.lower() in item['url'].lower() or search_query.lower() in item['title'].lower() or search_query.lower() in item['description'].lower()]

    # Limit the number of items if specified
    total_items = request.GET.get('total_items', 'all')  # Default number of items if not provided
    if total_items != 'all':
        seo_data = seo_data[:int(total_items)]  # Convert to int because GET parameters are always strings

    # Paginate the data
    paginator = Paginator(seo_data, 100)  # Increase PAGINATE_BY to see more results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_items = len(seo_data)

    # Define the path to the JSON file
    json_file_path = 'seo_data.json'

    # Check if the file exists
    if path.exists(json_file_path):
        # Get the time the file was last modified
        timestamp = stat(json_file_path).st_mtime
        # Convert the timestamp to a datetime object
        last_modified = datetime.fromtimestamp(timestamp)
    else:
        last_modified = None

    # Pass the last_modified date to the template
    return render(request, 'website_seo_overview.html', {'page_obj': page_obj, 'total_items': total_items, 'seo_data_total_length': seo_data_total_length, 'search_query': search_query, 'last_modified': last_modified})


class HomeView(TemplateView):
    template_name = "portfolio/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dan Poynor Visual/UX/Web Design & Development : Austin,TX 🤠'
        context['description'] = "UX/UI + ⚡️ Code: I solve business problems with creative strategy & technical expertise. I don't just make it pretty, I make it work."
        return context


class PortfolioView(TemplateView):
    template_name = "portfolio/portfolio.html"

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


class AboutView(TemplateView):
    template_name = "portfolio/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dan Poynor : UI/UX Design & Web Development : Austin, TX'
        context['description'] = "Multi-talented UX/UI design and development wiz with a proven track record of slaying digital dragons for diverse clients, big & small. Let's chat! 😀"
        return context


class ContactView(TemplateView):
    template_name = "portfolio/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Let’s Connect! : UI/UX Design & Web Development : Austin, TX'
        context['description'] = "I'm just a click, call, or email away. Let's discuss how we can transform your business. Send me your wildest ideas, and watch them become reality. 📲"
        return context


class ClientsView(TemplateView):
    template_name = "portfolio/client_list.html"

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
            "description": "From silicon giants to indie darlings, I've powered success for diverse clients. Explore my global portfolio & find your perfect design partner. ♥️",
        })

        return context


class ClientProjectsListView(PaginationMixin, PrevNextMixin, DetailView):
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

        context['title'] = f'{client_name} Design & Dev Projects : Austin, TX : Page {page} {order_text}'
        context['description'] = f'Explore design and development projects for {client_name}. Page {page} {order_text}.'
        return context


class IndustriesView(TemplateView):
    template_name = "portfolio/industry_list.html"

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


class IndustryProjectsListView(PaginationMixin, PrevNextMixin, DetailView):
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

        context['title'] = f'{industry_name} Design & Dev Projects : Austin, TX : Page {page} {order_text}'
        context['description'] = f'Explore design and development projects for {industry_name}. Page {page} {order_text}. ⚙️'
        return context


class MarketsView(TemplateView):
    template_name = "portfolio/market_list.html"

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
            "title": "Market-Driven Design & Development: View Tailored Solutions 🤑",
            "description": "From niche audiences to global markets, view my award-winning UX/UI & web solutions that speak their language. Built for success and maximum impact.",
        })

        return context


class MarketProjectsListView(PaginationMixin, PrevNextMixin, DetailView):
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


class MediaTypesView(TemplateView):
    template_name = "portfolio/mediatype_list.html"

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
            "description": "From print to interactive, design with seamless flexibility. Discover my media expertise & let's craft experiences that captivate. 🖨📺🕸",
        })

        return context


class MediaTypeProjectsListView(PaginationMixin, PrevNextMixin, DetailView):
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


class RolesView(TemplateView):
    template_name = "portfolio/role_list.html"

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
            "description": "Concept to code, I wear many hats. Explore my multi-faceted skillset & find the perfect design partner for your project. 🧢🎓🪖🎩",
        })

        return context


class RoleProjectsListView(PaginationMixin, PrevNextMixin, DetailView):
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


class ProjectsView(ListView):
    model = Project
    paginate_by = PAGINATE_BY
    template_name = "portfolio/project_list.html"
    view_name = "projects_page_order"
    paginator_template_name = "partials/pagination/_projects_paginator.html"

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
            visible=True,
            client__visible=True  # Check for visible client
        ).annotate(
            has_visible_items=Exists(has_visible_items_subquery)
        ).filter(
            has_visible_items=True
        )

        # Get the order from the URL, default to 'asc' if not provided
        order = self.kwargs.get("order", "asc")

        # Order the project list
        project_list = project_list.order_by('name' if order == 'asc' else '-name')

        return project_list

    def post(self, request, *args, **kwargs):
        # Get the selected order from the POST data
        order = request.POST.get("order", "asc")

        # Redirect to the first page with the selected order
        return redirect(self.view_name, page=1, order=order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the page number from the URL
        page_number = self.kwargs.get("page", '1')

        # Get the order from the URL, default to 'asc' if not provided
        order = self.kwargs.get("order", "asc")

        # Get the elided page range
        elided_page_range = context['paginator'].get_elided_page_range(context['page_obj'].number)

        # Create a title that includes the page number and order
        order_text = "Asc" if order == "asc" else "Desc"
        title = f"Visual/UX/UI Design & Software Development Successes - Page {page_number} {order_text}"

        context.update({
            "order": order,
            "count_type": "projects",  # Specify that we want to display the count of projects
            "view_name": self.view_name,  # The name of the current view
            "taxonomy_item_slug": "",  # There is no taxonomy item for this view
            "title": title,
            "description": DEFAULT_PAGE_DESCRIPTION,
            "paginator_template_name": self.paginator_template_name,
            "elided_page_range": elided_page_range,
        })

        return context


class ProjectItemsView(PrevNextMixin, DetailView):
    model = Project
    template_name = "portfolio/project_items_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.object.items.filter(visible=True)
        context["title"] = f'Project Items: {self.object.name}'
        context['description'] = DEFAULT_PAGE_DESCRIPTION
        return context


class ProjectDetailsView(ProjectDetailsPrevNextMixin, DetailView):
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
