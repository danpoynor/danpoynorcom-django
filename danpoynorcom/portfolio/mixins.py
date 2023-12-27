from django.db.models import Exists, OuterRef
from django.db.models.functions import Lower
from django.core.paginator import Paginator
from .models import Project


class PaginationMixin:
    paginate_by = 25

    def paginate_queryset(self, queryset, order_by='name'):
        order = self.request.GET.get('order', 'asc')
        if order == 'desc':
            queryset = queryset.order_by(f'-{order_by}')
        else:
            queryset = queryset.order_by(order_by)

        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        elided_page_range = paginator.get_elided_page_range(number=page_obj.number)

        return page_obj, order, elided_page_range, paginator.count


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
        current_index = ordered_items.index(current_object)

        # Get the previous and next items
        prev_item = ordered_items[current_index - 1] if ordered_items else None
        next_item = ordered_items[(current_index + 1) % len(ordered_items)] if ordered_items else None

        # Add the previous and next items to the context
        context['previous_object'] = prev_item
        context['next_object'] = next_item

        return context
