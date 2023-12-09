from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Case, When, IntegerField

from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem

admin.site.register(Client)
admin.site.register(Industry)
admin.site.register(Market)
admin.site.register(MediaType)
admin.site.register(Role)


class ProjectItemAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'visible', 'status', 'project_name')

    def project_name(self, obj):
        return obj.project.name if obj.project else '-'
    project_name.short_description = 'Project'


admin.site.register(ProjectItem, ProjectItemAdmin)


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'highlighted_name', 'visible', 'client_name', 'industries', 'markets', 'roles')

    def highlighted_name(self, obj):
        return format_html('<b>{}</b>', obj.name) if obj.name == '[Default Project]' else obj.name
    highlighted_name.short_description = 'Name'

    def client_name(self, obj):
        return obj.client.name if obj.client else '-'
    client_name.short_description = 'Client'

    def industries(self, obj):
        return ", ".join([industry.name for industry in obj.industry.all()])
    industries.short_description = 'Industries'

    def markets(self, obj):
        return ", ".join([market.name for market in obj.market.all()])
    markets.short_description = 'Markets'

    def roles(self, obj):
        return ", ".join([role.name for role in obj.role.all()])
    roles.short_description = 'Roles'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            is_default=Case(
                When(name='[Default Project]', then=0),
                default=1,
                output_field=IntegerField(),
            )
        ).order_by('is_default', 'name')

    def format_cell(self, obj, field):
        cell = super().format_cell(obj, field)
        if obj.name == '[Default Project]':
            return format_html('<b>{}</b>', cell)
        return cell


admin.site.register(Project, ProjectAdmin)
