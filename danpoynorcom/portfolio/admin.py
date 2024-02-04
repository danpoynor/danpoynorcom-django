from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.db.models import Case, When, IntegerField
from adminactions import actions

from .models import Client, Industry, Market, MediaType, Role, Project, ProjectItem, ProjectItemImage, ProjectItemAttachment

ROWS_PER_PAGE = 1000


class ClientAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("id", "visible", "name", "slug", "description", "items_count")
    list_display_links = ("name",)
    list_per_page = ROWS_PER_PAGE

    def items_count(self, obj):
        return obj.project_items.count()
    items_count.admin_order_field = 'items_count'  # make column sortable
    items_count.short_description = 'Items Count'

    def get_queryset(self, request):
        return super().get_queryset(request).model.all_objects.all()


class IndustryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("id", "visible", "name", "slug", "description", "items_count")
    list_display_links = ("name",)
    list_per_page = ROWS_PER_PAGE

    def items_count(self, obj):
        return obj.project_items.count()
    items_count.admin_order_field = 'items_count'  # make column sortable
    items_count.short_description = 'Items Count'

    def get_queryset(self, request):
        return super().get_queryset(request).model.all_objects.all()


class MarketAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("id", "visible", "name", "slug", "description", "items_count")
    list_display_links = ("name",)
    list_per_page = ROWS_PER_PAGE

    def items_count(self, obj):
        return obj.project_items.count()
    items_count.admin_order_field = 'items_count'  # make column sortable
    items_count.short_description = 'Items Count'

    def get_queryset(self, request):
        return super().get_queryset(request).model.all_objects.all()


class MediaTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("id", "visible", "name", "slug", "description", "items_count")
    list_display_links = ("name",)
    list_per_page = ROWS_PER_PAGE

    def items_count(self, obj):
        return obj.project_items.count()
    items_count.admin_order_field = 'items_count'  # make column sortable
    items_count.short_description = 'Items Count'

    def get_queryset(self, request):
        return super().get_queryset(request).model.all_objects.all()


class RoleAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("id", "visible", "name", "slug", "description", "items_count")
    list_display_links = ("name",)
    list_per_page = ROWS_PER_PAGE

    def items_count(self, obj):
        return obj.project_items.count()
    items_count.admin_order_field = 'items_count'  # make column sortable
    items_count.short_description = 'Items Count'

    def get_queryset(self, request):
        return super().get_queryset(request).model.all_objects.all()


class ProjectItemImageInline(admin.StackedInline):
    model = ProjectItemImage
    extra = 0


class ProjectItemImageAdmin(admin.ModelAdmin):
    search_fields = ["original"]
    list_display = ("id", "admin_list_thumb", "thumbnail", "medium", "medium_large", "large", "original")
    list_per_page = ROWS_PER_PAGE


class ProjectItemAttachmentInline(admin.StackedInline):
    model = ProjectItemAttachment
    extra = 0


class ProjectItemAttachmentAdmin(admin.ModelAdmin):
    search_fields = ["file"]
    list_display = ("id", "visible", "file", "link_text")
    list_per_page = ROWS_PER_PAGE


class ProjectItemAdmin(admin.ModelAdmin):
    search_fields = ["name", "project__name"]
    list_display = ("id", "visible", "name", "status", "project_name", "client_name", "industries", "markets", "media_types", "roles", "year", "item_order")
    list_display_links = ("name",)
    inlines = [ProjectItemImageInline, ProjectItemAttachmentInline]
    actions = [actions.mass_update]
    list_per_page = ROWS_PER_PAGE

    def get_queryset(self, request):
        return ProjectItem.all_objects.get_queryset().select_related('project')  # Use all_objects manager

    def project_name(self, obj):
        return obj.project.name if obj.project else "-"
    project_name.short_description = "Project"
    project_name.admin_order_field = 'project__name'  # Allows column order sorting

    def client_name(self, obj):
        return obj.client.name if obj.client else "-"
    client_name.short_description = "Client"

    def media_types(self, obj):
        return ", ".join([media_type.name for media_type in obj.media_type.all()])
    media_types.short_description = "Media Types"

    def industries(self, obj):
        return ", ".join([industry.name for industry in obj.industry.all()])
    industries.short_description = "Industries"

    def markets(self, obj):
        return ", ".join([market.name for market in obj.market.all()])
    markets.short_description = "Markets"

    def roles(self, obj):
        return ", ".join([role.name for role in obj.role.all()])
    roles.short_description = "Roles"


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ["name", "slug"]
    list_display = ("id", "visible", "name", "description", "items_count")
    list_display_links = ("name",)
    list_per_page = ROWS_PER_PAGE

    def items_count(self, obj):
        return obj.items_count
    items_count.admin_order_field = 'items_count'  # make column sortable
    items_count.short_description = 'Items Count'

    def get_queryset(self, request):
        qs = Project.all_objects.get_queryset()  # Use all_objects manager
        qs = qs.annotate(
            items_count=Count('item'),  # add items_count field
            is_default=Case(
                When(name="[Default Project]", then=0),
                default=1,
                output_field=IntegerField(),
            )
        )
        return qs.order_by("is_default", "name")

    def format_cell(self, obj, field):
        cell = super().format_cell(obj, field)
        if obj.name == "[Default Project]":
            return format_html("<b>{}</b>", cell)
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
