import re
import random
import inflect
from django.db.models import OuterRef, Exists
from django.shortcuts import redirect
from django.db.models.functions import Lower
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from ..models import Client, Industry, Market, MediaType, Role, Project, ProjectItem
from ..mixins import PaginationMixin
from ..constants import DEFAULT_PAGE_DESCRIPTION, PAGINATE_BY


# Select random word or phrase to use at the beginning of the page titles or descriptions
def random_synonym_for_explore():
    synonyms_for_explore = [
        "✅ Approved",
        "🚥 Analyze",
        "🏆 Award winning",
        "👁 Be amazed by",
        "🤩 Be blown away by",
        "⭐️ Browse the best",
        "🔭 Check out",
        "😎 Cool",
        "😻 Discover",
        "💀 Examine killer",
        "👌 Excellent",
        "😍 Experience the best",
        "👽 Explore incredible",
        "👁 Eye my",
        "🌚 Eyeball these",
        "💜 Fantastic",
        "🐸 Get a peek at",
        "😉 Good examples of",
        "👍 Great",
        "😳 Incredible",
        "🧐 Inspect my",
        "👀 Look at",
        "👍 Like my",
        "👉 Look into",
        "⭐️ Outstanding",
        "😹 Peruse",
        "🟢 Research top",
        "🕵️ Spy on",
        "👩🏼 Study",
        "🔎 Survey expert",
        "🎩 Tip top",
        "👋 View my",
    ]
    return random.choice(synonyms_for_explore)


def get_taxonomy_objects_with_visible_projects(TaxonomyModel):
    # Subquery to check if a taxonomy object has any visible projects with visible items
    has_visible_projects_with_visible_items_subquery = Project.visible_objects.filter(
        **{TaxonomyModel._meta.model_name: OuterRef("pk")},
        item__visible=True  # Check for visible items
    )

    # Get taxonomy objects that have any visible projects with visible items
    taxonomy_objects = TaxonomyModel.visible_objects.annotate(
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


class ClientProjectsListView(PaginationMixin, DetailView):
    model = Client
    template_name = "portfolio/client_detail.html"
    count_type = "client items"
    view_name = "client_page_order"
    filter_field = "client"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_name = self.object.name.title()
        words = re.split(r'(\s|/)', client_name)
        words = [capitalize_special_words(word) for word in words]
        client_name = "".join(words)
        # Check if ".Com" is in the name and replace it with ".com"
        if ".Com" in client_name:
            client_name = client_name.replace(".Com", ".com")

        context['title'] = f'{client_name} Design & Dev Projects : Austin, TX : Page {context["page"]} {context["order_text"]}'
        context['description'] = f'{random_synonym_for_explore()} design and development projects for {client_name}'
        context['previous_object'] = self.object.get_previous()
        context['next_object'] = self.object.get_next()
        return context


class IndustryProjectsListView(PaginationMixin, DetailView):
    model = Industry
    template_name = "portfolio/industry_detail.html"
    count_type = "industry items"
    view_name = "industry_page_order"
    filter_field = "industry"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        industry_name = self.object.name.title()
        words = re.split(r'(\s|/)', industry_name)
        words = [capitalize_special_words(word) for word in words]
        industry_name = "".join(words)
        # Check if "Projects" is already in the name
        if "Projects" in industry_name:
            industry_name = industry_name.replace("Projects", "").strip()

        context['title'] = f'{industry_name} Design & Dev Projects : Austin, TX : Page {context["page"]} {context["order_text"]}'
        context['description'] = f'{random_synonym_for_explore()} design and development projects for {industry_name}'
        context['previous_object'] = self.object.get_previous()
        context['next_object'] = self.object.get_next()
        return context


class MarketProjectsListView(PaginationMixin, DetailView):
    model = Market
    template_name = "portfolio/market_detail.html"
    count_type = "market items"
    view_name = "market_page_order"
    filter_field = "market"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.name} Design & Development Expertise :  Austin, TX : Page {context["page"]} {context["order_text"]}'
        context['description'] = f'{random_synonym_for_explore()} design and development projects for {self.object.name}'
        context['previous_object'] = self.object.get_previous()
        context['next_object'] = self.object.get_next()
        return context


class MediaTypeProjectsListView(PaginationMixin, DetailView):
    model = MediaType
    template_name = "portfolio/media_type_detail.html"
    count_type = "media type items"
    view_name = "media_type_page_order"
    filter_field = "media_type"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
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

        # Check if "Design" is already in the name
        if "Design" in singular_name or "Video Editing" in singular_name or "Photography" in singular_name:
            context['title'] = f'{singular_name} Portfolio : Austin, TX : Page {context["page"]} {context["order_text"]}'
            context['description'] = f'{random_synonym_for_explore()} {singular_name} portfolio. Page {context["page"]} {context["order_text"]}'
        else:
            context['title'] = f'{singular_name} Designer Portfolio : Austin, TX : Page {context["page"]} {context["order_text"]}'
            context['description'] = f'{random_synonym_for_explore()} {singular_name} designer portfolio'
        context['previous_object'] = self.object.get_previous()
        context['next_object'] = self.object.get_next()
        return context


class RoleProjectsListView(PaginationMixin, DetailView):
    model = Role
    template_name = "portfolio/role_detail.html"
    count_type = "role items"
    view_name = "role_page_order"
    filter_field = "role"
    paginator_template_name = "partials/pagination/_paginator.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role_name = self.object.name.title()
        words = re.split(r'(\s|/)', role_name)
        words = [capitalize_special_words(word) for word in words]
        role_name = "".join(words)

        context['title'] = f'{role_name} Portfolio : Austin, TX : Page {context["page"]} {context["order_text"]}'
        context['description'] = f'{random_synonym_for_explore()} {role_name} portfolio'
        context['previous_object'] = self.object.get_previous()
        context['next_object'] = self.object.get_next()
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
        has_visible_items_subquery = ProjectItem.visible_objects.filter(
            project=OuterRef("pk")
        )

        # Get projects that have any visible items
        project_list = Project.visible_objects.annotate(
            has_visible_items=Exists(has_visible_items_subquery)
        ).filter(
            has_visible_items=True
        )

        # Get the order from the URL, default to 'asc' if not provided
        order = self.kwargs.get("order", "asc")

        # Order the project list
        project_list = project_list.order_by(Lower('name') if order == 'asc' else Lower('name').desc())

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
