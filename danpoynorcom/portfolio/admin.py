from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Case, When, IntegerField

from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem, ProjectItemImage, ProjectItemAttachment


class ClientAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'slug', 'description')
    list_display_links = ('name',)


class IndustryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'slug', 'description')
    list_display_links = ('name',)


class MarketAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'slug', 'description')
    list_display_links = ('name',)


class MediaTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'slug', 'description')
    list_display_links = ('name',)


class RoleAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'slug', 'description')
    list_display_links = ('name',)


class ProjectItemImageInline(admin.StackedInline):
    model = ProjectItemImage
    extra = 0


class ProjectItemImageAdmin(admin.ModelAdmin):
    search_fields = ['file']
    list_display = ('id', 'admin_list_thumb', 'thumbnail', 'medium', 'medium_large', 'large', 'original')


class ProjectItemAttachmentInline(admin.StackedInline):
    model = ProjectItemAttachment
    extra = 0


class ProjectItemAttachmentAdmin(admin.ModelAdmin):
    search_fields = ['file']
    list_display = ('id', 'file', 'link_text', 'visible')


class ProjectItemAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'visible', 'status', 'project_name', 'item_order')
    list_display_links = ('name',)
    inlines = [ProjectItemImageInline, ProjectItemAttachmentInline]

    def project_name(self, obj):
        return obj.project.name if obj.project else '-'
    project_name.short_description = 'Project'


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'visible', 'client_name', 'media_types', 'industries', 'markets', 'roles', 'year')
    list_display_links = ('name',)

    def client_name(self, obj):
        return obj.client.name if obj.client else '-'
    client_name.short_description = 'Client'

    def media_types(self, obj):
        return ", ".join([media_type.name for media_type in obj.mediatype.all()])
    media_types.short_description = 'Media Types'

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


# Register the models
admin.site.register(Client, ClientAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Market, MarketAdmin)
admin.site.register(MediaType, MediaTypeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(ProjectItem, ProjectItemAdmin)
admin.site.register(ProjectItemImage, ProjectItemImageAdmin)
admin.site.register(ProjectItemAttachment, ProjectItemAttachmentAdmin)
admin.site.register(Project, ProjectAdmin)
