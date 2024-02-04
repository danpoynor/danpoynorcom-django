from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem

PAGINATE_BY = 24
SELECTED_CLIENT_IDS = [42, 65, 4, 83, 37]
SELECTED_INDUSTRY_IDS = [13, 32, 8, 3, 21]
SELECTED_MEDIA_TYPE_IDS = [28, 3, 21, 36, 38]
SELECTED_ROLE_IDS = [12, 24, 22, 2, 8]
HIGHLIGHTED_INDUSTRY_IDS = [3, 13, 32, 8, 21, 24]
HIGHLIGHTED_MEDIA_TYPE_IDS = [28, 3, 21, 36, 38]
HIGHLIGHTED_ROLE_IDS = [12, 24, 22, 2, 8]
VIEW_NAMES = ['home', 'portfolio', 'about', 'contact', 'client_list', 'industry_list', 'market_list', 'mediatype_list', 'role_list']
MODELS = [Client, Industry, Market, MediaType, Role, Project, ProjectItem]
DEFAULT_PAGE_DESCRIPTION = "Dan Poynor is a UI/UX designer and web developer in Austin, TX. He has worked with clients in a wide range of industries and markets, including startups, small businesses, and global brands."
