from django.db.models.functions import Lower
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.http import Http404
from .models import ProjectItem
from .constants import PAGINATE_BY


class PaginationMixin:
    paginator_template_name = "partials/pagination/_paginator.html"
    paginate_by = PAGINATE_BY
    count_type = None
    view_name = None
    filter_field = None

    def post(self, request, *args, **kwargs):
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

        # orphans note: If the last page would have fewer items than this
        # number, those items are added to the previous page.
        paginator = Paginator(queryset, self.paginate_by, orphans=3)

        # Check if the requested page number is greater than the total number of pages
        page_number = int(page_number)  # Convert page_number to an integer
        if page_number > paginator.num_pages:
            raise Http404("Page not found")

        # Check if the order parameter is either 'asc' or 'desc'
        if order not in ['asc', 'desc']:
            raise Http404("Page not found")

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
            visible_projects = ProjectItem.visible_objects.filter(**filter_kwargs)
        else:
            # If no filter field is specified, get all visible projects
            visible_projects = ProjectItem.visible_objects.all()

        # Get the page number and order from the request's query parameters
        page = self.kwargs.get('page', '1')
        order = self.kwargs.get('order', 'asc')
        order_text = "Asc" if order == "asc" else "Desc"

        # Fetch the related ProjectItem objects
        items = ProjectItem.visible_objects.filter(**{self.filter_field: self.object})

        # Paginate items
        page_obj, order, elided_page_range, total_projects = self.paginate_queryset(items, page, order)

        # Convert the elided page range to a list
        pages = list(elided_page_range)

        context.update({
            "paginator_template_name": self.paginator_template_name,
            "page_obj": page_obj,
            "order": order,
            "order_text": order_text,
            "page": page_obj.number,
            "pages": pages,
            "total_projects": total_projects,
            "count_type": self.count_type,  # Specify that we want to display the count of items
            "view_name": self.view_name,  # The name of the current view
            "taxonomy_item_slug": getattr(self, 'object', None) and self.object.slug,  # The object's slug
        })

        return context
