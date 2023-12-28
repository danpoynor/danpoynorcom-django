from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

# Make sure the "portfolio" module is installed and accessible in the Python environment
try:
    from portfolio import views
except ImportError:
    # if the module is not installed, use the "portfolio" module in the current directory
    from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("portfolio/clients/", views.clients, name="clients"),
    path("portfolio/clients/<slug:slug>/", views.ClientProjectsListView.as_view(), name="client_detail"),
    path("portfolio/industries/", views.industries, name="industries"),
    path("portfolio/industries/<slug:slug>/", views.IndustryProjectsListView.as_view(), name="industry_detail"),
    path("portfolio/markets/", views.markets, name="markets"),
    path("portfolio/markets/<slug:slug>/", views.MarketProjectsListView.as_view(), name="market_detail"),
    path("portfolio/media-types/", views.mediatypes, name="mediatypes"),
    path("portfolio/media-types/<slug:slug>/", views.MediaTypeProjectsListView.as_view(), name="mediatype_detail"),
    path("portfolio/roles/", views.roles, name="roles"),
    path("portfolio/roles/<slug:slug>/", views.RoleProjectsListView.as_view(), name="role_detail"),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("portfolio/projects/<slug:slug>/", views.ProjectItemsView.as_view(), name="project"),
    path("portfolio/project-details/<slug:slug>/", views.ProjectDetailsView.as_view(), name="project_detail"),
    path("legal-notice-to-picscout-getty-images-picscout-clients-cyveillance-you-are-prohibited-from-accessing-this-site/", views.getty_legal_notice, name="getty_legal_notice"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("pages/", include("django.contrib.flatpages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
