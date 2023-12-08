from django.contrib import admin

from .models import Client
from .models import Industry
from .models import Market
from .models import MediaType
from .models import Role
from .models import Project
from .models import ProjectItem

admin.site.register(Client)
admin.site.register(Industry)
admin.site.register(Market)
admin.site.register(MediaType)
admin.site.register(Role)
admin.site.register(Project)
admin.site.register(ProjectItem)
