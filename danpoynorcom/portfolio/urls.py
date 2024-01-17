import django
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ClientSitemap, IndustrySitemap, MarketSitemap, MediaTypeSitemap, RoleSitemap, ProjectSitemap, ProjectItemDetailSitemap

# Make sure the "portfolio" module is installed and accessible in the Python environment
try:
    from portfolio import views
except ImportError:
    # if the module is not installed, use the "portfolio" module in the current directory
    from . import views


def custom_page_not_found(request):
    return django.views.defaults.page_not_found(request, None)


sitemaps = {
    'static': StaticViewSitemap,
    'client': ClientSitemap,
    'industry': IndustrySitemap,
    'market': MarketSitemap,
    'mediatype': MediaTypeSitemap,
    'role': RoleSitemap,
    'project': ProjectSitemap,
    'projectitemdetail': ProjectItemDetailSitemap,
    # 'projectitems': ProjectItemsSitemap, # These have similar content to ProjectItemDetailSitemap
}

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("portfolio/", views.PortfolioView.as_view(), name="portfolio"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),

    path("portfolio/clients/", views.ClientsView.as_view(), name="client_list"),
    path("portfolio/clients/<slug:slug>-projects/", views.ClientProjectsListView.as_view(), name="client_detail"),
    path("portfolio/clients/<slug:slug>-projects/<int:page>/<str:order>/", views.ClientProjectsListView.as_view(), name="client_page_order"),

    path("portfolio/industries/", views.IndustriesView.as_view(), name="industry_list"),
    path("portfolio/industries/<slug:slug>-projects/", views.IndustryProjectsListView.as_view(), name="industry_detail"),
    path("portfolio/industries/<slug:slug>-projects/<int:page>/<str:order>/", views.IndustryProjectsListView.as_view(), name="industry_page_order"),

    path("portfolio/markets/", views.MarketsView.as_view(), name="market_list"),
    path("portfolio/markets/<slug:slug>-projects/", views.MarketProjectsListView.as_view(), name="market_detail"),
    path("portfolio/markets/<slug:slug>-projects/<int:page>/<str:order>/", views.MarketProjectsListView.as_view(), name="market_page_order"),

    path("portfolio/media-types/", views.MediaTypesView.as_view(), name="mediatype_list"),
    path("portfolio/media-types/<slug:slug>-projects/", views.MediaTypeProjectsListView.as_view(), name="mediatype_detail"),
    path("portfolio/media-types/<slug:slug>-projects/<int:page>/<str:order>/", views.MediaTypeProjectsListView.as_view(), name="mediatype_page_order"),

    path("portfolio/roles/", views.RolesView.as_view(), name="role_list"),
    path("portfolio/roles/<slug:slug>-projects/", views.RoleProjectsListView.as_view(), name="role_detail"),
    path("portfolio/roles/<slug:slug>-projects/<int:page>/<str:order>/", views.RoleProjectsListView.as_view(), name="role_page_order"),

    path("portfolio/design-and-development-projects/", views.ProjectsView.as_view(), name="project_list"),
    path('portfolio/design-and-development-projects/<int:page>/', views.ProjectsView.as_view(), name='projects_page'),
    path('portfolio/design-and-development-projects/<int:page>/<str:order>/', views.ProjectsView.as_view(), name='projects_page_order'),
    path('portfolio/design-and-development-projects/<int:page>/<str:order>/<str:slug>/', views.ProjectsView.as_view(), name='projects_page_order_slug'),

    path("portfolio/design-and-development-projects/<slug:slug>/", views.ProjectItemsView.as_view(), name="project_items_detail"),
    path("portfolio/project-details/<slug:slug>/", views.ProjectDetailsView.as_view(), name="project_detail"),

    # Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),


    # Robots.txt
    # path("robots.txt", views.robots, name="robots"),

    # Test the 404 page at http://localhost:8000/404/
    path("404/", custom_page_not_found),

    # Page created for use with wget
    path('wget_sitemap/', views.WgetSitemapView.as_view(), name='wget_sitemap'),

    # Page created for reviewing some SEO factors of each page
    path('website-seo-overview/', views.WebsiteSeoView.as_view(), name='website_seo_overview'),

    path("__debug__/", include("debug_toolbar.urls")),
    path("pages/", include("django.contrib.flatpages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
