from django.urls import path

from portfolio import views

urlpatterns = [
    path("", views.home, name="home"),
    path("portfolio", views.portfolio, name="portfolio"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("portfolio/clients", views.clients, name="clients"),
    path('portfolio/clients/<slug:slug>/', views.ClientDetailView.as_view(), name='client_detail'),
    path("portfolio/industries", views.industries, name="industries"),
    path('portfolio/industries/<slug:slug>/', views.IndustryDetailView.as_view(), name='industry_detail'),
    path("portfolio/markets", views.markets, name="markets"),
    path('portfolio/markets/<slug:slug>/', views.MarketDetailView.as_view(), name='market_detail'),
    path("portfolio/mediatypes", views.mediatypes, name="mediatypes"),
    path('portfolio/mediatypes/<slug:slug>/', views.MediaTypeDetailView.as_view(), name='mediatype_detail'),
    path("portfolio/roles", views.roles, name="roles"),
    path('portfolio/roles/<slug:slug>/', views.RoleDetailView.as_view(), name='role_detail'),
    path("portfolio/projects", views.projects, name="projects"),
    path('portfolio/project-details/<slug:slug>/', views.ProjectDetailsView.as_view(), name='project_detail'),
]
