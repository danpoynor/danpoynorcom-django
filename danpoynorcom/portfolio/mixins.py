from django.db.models import Exists, OuterRef
from django.db.models.functions import Lower
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from .models import Project, ProjectItem
from .constants import PAGINATE_BY
from .utils import get_visible_objects


class PaginationMixin:
    paginator_template_name = "partials/pagination/_paginator.html"
    paginate_by = PAGINATE_BY
    count_type = None
    view_name = None
    filter_field = None

    def post(self, request):
        # Get the selected order from the POST data
        order = request.POST.get('order', 'asc')

        # Get the slug from the URL
        slug = self.kwargs.get('slug')

        # Redirect to the first page with the selected order
        return redirect(self.view_name, slug=slug, page=1, order=order)

    def paginate_queryset(self, queryset, page_number, order='asc'):
        if order == 'desc':
            queryset = queryset.order_by(Lower('name').desc())
        else:
            queryset = queryset.order_by(Lower('name'))

        paginator = Paginator(queryset, self.paginate_by)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_obj = paginator.page(paginator.num_pages)

        elided_page_range = paginator.get_elided_page_range(number=page_obj.number)

        return page_obj, order, elided_page_range, paginator.count

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get visible projects
        if self.filter_field is not None:
            # If a filter field is specified, filter by the current object
            filter_kwargs = {self.filter_field: self.object}
            visible_projects = get_visible_objects(Project).filter(**filter_kwargs)
        else:
            # If no filter field is specified, get all visible projects
            visible_projects = get_visible_objects(Project)

        # Get visible items for the visible projects
        all_items = get_visible_objects(ProjectItem).filter(project__in=visible_projects)

        # Get the page number and order from the URL
        page = self.kwargs.get('page')
        order = self.kwargs.get('order', 'asc')

        # Paginate items
        page_obj, order, elided_page_range, total_projects = self.paginate_queryset(all_items, page, order)

        context.update({
            "paginator_template_name": self.paginator_template_name,
            "page_obj": page_obj,
            "order": order,
            "pages": elided_page_range,
            "total_projects": total_projects,
            "count_type": self.count_type,  # Specify that we want to display the count of items
            "view_name": self.view_name,  # The name of the current view
            "taxonomy_item_slug": getattr(self, 'object', None) and self.object.slug,  # The object's slug
        })

        return context


class PrevNextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ensure self.object and self.model are not None
        if self.object is None or self.model is None:
            return context

        # Get the current object
        current_object = self.object

        # Check if the model is Project
        if self.model == Project:
            # Filter Project objects directly
            has_visible_projects_with_visible_items_subquery = Project.objects.filter(
                visible=True,
                item__visible=True  # Check for visible items
            )
        else:
            # Filter Project objects based on a dynamic field name
            has_visible_projects_with_visible_items_subquery = Project.objects.filter(
                **{self.model._meta.model_name: OuterRef('pk')},
                visible=True,
                item__visible=True  # Check for visible items
            )

        # Annotate the objects with the has_visible_projects_with_visible_items field
        objects = self.model.objects.annotate(
            has_visible_projects_with_visible_items=Exists(has_visible_projects_with_visible_items_subquery)
        )

        # Get the previous object
        previous_object = objects.filter(
            id__lt=current_object.id,
            has_visible_projects_with_visible_items=True,
            visible=True  # Ensure the term itself is visible
        ).order_by('-id').first()
        if previous_object is None:
            # If there is no previous object, get the last object
            previous_object = objects.filter(
                has_visible_projects_with_visible_items=True,
                visible=True  # Ensure the term itself is visible
            ).order_by('-id').first()

        # Get the next object
        next_object = objects.filter(
            id__gt=current_object.id,
            has_visible_projects_with_visible_items=True,
            visible=True  # Ensure the term itself is visible
        ).order_by('id').first()
        if next_object is None:
            # If there is no next object, get the first object
            next_object = objects.filter(
                has_visible_projects_with_visible_items=True,
                visible=True  # Ensure the term itself is visible
            ).order_by('id').first()

        context['previous_object'] = previous_object
        context['next_object'] = next_object

        return context


class ProjectDetailsPrevNextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current object
        current_object = self.object

        # Get all visible Projects ordered by client name and then by name
        ordered_projects = Project.objects.filter(visible=True, client__visible=True).order_by(Lower('client__name'), Lower('name'))

        # Get all visible ProjectItem objects ordered by their project's name and their order within the project
        ordered_items = []
        for project in ordered_projects:
            ordered_items.extend(list(project.get_ordered_items().filter(visible=True)))

        # Get the index of the current object in the ordered items
        # The if/else check is to prevent a ValueError in tests when current_object is not in ordered_items
        if current_object in ordered_items:
            current_index = ordered_items.index(current_object)
        else:
            current_index = None

        # Get the previous and next items
        prev_item = ordered_items[current_index - 1] if ordered_items else None
        next_item = ordered_items[(current_index + 1) % len(ordered_items)] if ordered_items else None

        # Add the previous and next items to the context
        context['previous_object'] = prev_item
        context['next_object'] = next_item

        return context
