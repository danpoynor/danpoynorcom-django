from django.db.models.functions import Lower
from django.views.generic import TemplateView, DetailView
from ..models import Client, Industry, Market, MediaType, Role, Project, ProjectItem
from ..constants import DEFAULT_PAGE_DESCRIPTION, SELECTED_CLIENT_IDS, SELECTED_INDUSTRY_IDS, SELECTED_MEDIA_TYPE_IDS, SELECTED_ROLE_IDS, HIGHLIGHTED_INDUSTRY_IDS, HIGHLIGHTED_MEDIA_TYPE_IDS, HIGHLIGHTED_ROLE_IDS


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

        selected_clients = Client.visible_objects.filter(id__in=SELECTED_CLIENT_IDS)
        for client in selected_clients:
            client.project_item_count = ProjectItem.visible_objects.filter(client=client).count()

        selected_industries = Industry.visible_objects.filter(id__in=SELECTED_INDUSTRY_IDS)
        for industry in selected_industries:
            industry.project_item_count = ProjectItem.visible_objects.filter(industry=industry).count()

        selected_media_types = MediaType.visible_objects.filter(id__in=SELECTED_MEDIA_TYPE_IDS)
        for media_type in selected_media_types:
            media_type.project_item_count = ProjectItem.visible_objects.filter(media_type=media_type).count()

        selected_roles = Role.visible_objects.filter(id__in=SELECTED_ROLE_IDS)
        for role in selected_roles:
            role.project_item_count = ProjectItem.visible_objects.filter(role=role).count()

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
        context['description'] = "I'm just a click, call, or email away. Let's discuss how we can transform your business. Send me your wildest ideas, and watch them become reality 🤝"
        return context


class ClientsView(TemplateView):
    template_name = "portfolio/client_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        client_list = Client.visible_objects.all().order_by(Lower("name"))
        for client in client_list:
            # Get visible items for the current client
            visible_project_items = ProjectItem.visible_objects.filter(client=client)

            # Count the number of visible items for the current client
            client.project_item_count = visible_project_items.count()

        context.update({
            "clients": client_list,
            "object": Client(),
            "title": "Startups to Global Brands : Checkout My Design & Dev Clients",
            "description": "From silicon giants to indie darlings, I've powered success for diverse clients. Explore my global portfolio & find your perfect design partner 💓",
        })

        return context


class IndustriesView(TemplateView):
    template_name = "portfolio/industry_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        highlighted_industries = Industry.visible_objects.filter(id__in=HIGHLIGHTED_INDUSTRY_IDS)
        for industry in highlighted_industries:
            visible_project_items = ProjectItem.visible_objects.filter(industry=industry)
            industry.project_item_count = visible_project_items.count()

        industry_list = Industry.visible_objects.all().order_by(Lower("name"))
        for industry in industry_list:
            visible_project_items = ProjectItem.visible_objects.filter(industry=industry)
            industry.project_item_count = visible_project_items.count()

        market_list = Market.visible_objects.all().order_by(Lower("name"))
        for market in market_list:
            visible_project_items = ProjectItem.visible_objects.filter(market=market)
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


class MarketsView(TemplateView):
    template_name = "portfolio/market_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        market_list = Market.visible_objects.all().order_by(Lower("name"))
        for market in market_list:
            # Get visible items for the current market
            visible_project_items = ProjectItem.visible_objects.filter(market=market)

            market.project_item_count = visible_project_items.count()

        context.update({
            "markets": market_list,
            "object": Market(),
            "title": "Market-Driven Design & Development: View Tailored Solutions 🤑",
            "description": "From niche audiences to global markets, view my award-winning UX/UI & web solutions that speak their language. Built for success and maximum impact.",
        })

        return context


class MediaTypesView(TemplateView):
    template_name = "portfolio/media_type_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        highlighted_media_types = MediaType.visible_objects.filter(id__in=HIGHLIGHTED_MEDIA_TYPE_IDS)
        for media_type in highlighted_media_types:
            visible_project_items = ProjectItem.visible_objects.filter(media_type=media_type)
            media_type.project_item_count = visible_project_items.count()

        media_type_list = MediaType.visible_objects.all().order_by(Lower("name"))
        for media_type in media_type_list:
            visible_project_items = ProjectItem.visible_objects.filter(media_type=media_type)
            media_type.project_item_count = visible_project_items.count()

        context.update({
            "highlighted_media_types": highlighted_media_types,
            "mediatypes": media_type_list,
            "object": MediaType(),
            "title": "Pixels 2 Print & Beyond : View Engaging Design & Dev Mastery",
            "description": "From print to interactive, design with seamless flexibility. Discover my media expertise & let's craft experiences that captivate 🕸",
        })

        return context


class RolesView(TemplateView):
    template_name = "portfolio/role_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        highlighted_roles = Role.visible_objects.filter(id__in=HIGHLIGHTED_ROLE_IDS)
        for role in highlighted_roles:
            visible_project_items = ProjectItem.visible_objects.filter(role=role)
            role.project_item_count = visible_project_items.count()

        role_list = Role.visible_objects.all().order_by(Lower("name"))
        for role in role_list:
            visible_project_items = ProjectItem.visible_objects.filter(role=role)
            role.project_item_count = visible_project_items.count()

        context.update({
            "highlighted_roles": highlighted_roles,
            "roles": role_list,
            "object": Role(),
            "title": "Concept to Creation: View My Diverse Design & Dev Experience",
            "description": "Concept to code, I wear many hats. Explore my multi-faceted skill set & find the perfect design partner for your project 🧢🎓🎩",
        })

        return context


class ProjectItemsView(DetailView):
    model = Project
    template_name = "portfolio/project_items_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.object.items.filter(visible=True)
        context["title"] = f'Project Items: {self.object.name}'
        context['description'] = DEFAULT_PAGE_DESCRIPTION
        return context


class ProjectDetailsView(DetailView):
    model = ProjectItem
    template_name = "portfolio/project_detail.html"

    def get_class_name(self):
        return self.__class__.__name__

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object.project
        context["items"] = ProjectItem.visible_objects.filter(project=project).order_by('item_order')

        # Check if project item name and project name are the same
        if self.object.name == project.name:
            context['title'] = f'Project: {self.object.name}'
            context['description'] = f'View Details: {self.object.name}'
        else:
            context['title'] = f'Project: {project.name} : {self.object.name}'
            context['description'] = f'View Details: {project.name} and item: {self.object.name}'

        context['previous_object'] = self.object.get_previous()
        context['next_object'] = self.object.get_next()
        return context
