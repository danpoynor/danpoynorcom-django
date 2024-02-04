import datetime
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.db.models import Count, OuterRef, Q
from django.urls import reverse
from django.db import models
from django.db.models.functions import Lower


# Custom managers
class VisibleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visible=True).order_by(Lower('name'))


class ProjectItemVisibleManager(models.Manager):
    def get_queryset(self):
        # Subqueries for many-to-many relations
        industries = Industry.visible_objects.filter(project_item=OuterRef('pk'), visible=False)
        markets = Market.visible_objects.filter(project_item=OuterRef('pk'), visible=False)
        media_types = MediaType.visible_objects.filter(project_item=OuterRef('pk'), visible=False)
        roles = Role.visible_objects.filter(project_item=OuterRef('pk'), visible=False)

        return super().get_queryset().filter(
            Q(visible=True),
            Q(project__visible=True),
            Q(client__visible=True),
            ~Q(id__in=industries),
            ~Q(id__in=markets),
            ~Q(id__in=media_types),
            ~Q(id__in=roles),
        ).distinct()


class TaxonomyMixin(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def get_verbose_name(self):
        return self._meta.verbose_name

    def get_verbose_name_plural(self):
        return self._meta.verbose_name_plural

    def get_project_items(self):
        return self.project_items.all()

    def has_projects(self):
        # Check if term has at least one Project with at least one ProjectItem
        return self.project_items.filter(project__item__isnull=False).exists()

    def get_absolute_url(self):
        return reverse(f"{self._meta.model_name}_detail", args=[str(self.slug)])

    def get_next(self):
        next_item = (self.__class__.visible_objects.annotate(lower_name=Lower('name'), num_project_items=Count('project_item'))
                     .filter(lower_name__gt=self.name.lower(), num_project_items__gt=0)
                     .order_by('lower_name')
                     .first())
        if next_item is None:
            next_item = (self.__class__.visible_objects.annotate(lower_name=Lower('name'), num_project_items=Count('project_item'))
                         .filter(num_project_items__gt=0)
                         .order_by('lower_name')
                         .first())
        return next_item

    def get_previous(self):
        previous_item = (self.__class__.visible_objects.annotate(lower_name=Lower('name'), num_project_items=Count('project_item'))
                         .filter(lower_name__lt=self.name.lower(), num_project_items__gt=0)
                         .order_by('-lower_name')
                         .first())
        if previous_item is None:
            previous_item = (self.__class__.visible_objects.annotate(lower_name=Lower('name'), num_project_items=Count('project_item'))
                             .filter(num_project_items__gt=0)
                             .order_by('-lower_name')
                             .first())
        return previous_item


# Client taxonomy model
class Client(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["name"]
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False)
    description = models.TextField(help_text="Enter the client description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the client should be visible")
    logo = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    website = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    visible_objects = VisibleManager()
    all_objects = models.Manager()


# Industry taxonomy model
class Industry(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
        ordering = ["name"]
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False)
    description = models.TextField(help_text="Enter the industry description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the industry should be visible")
    image_sm = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_md = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_lg = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    visible_objects = VisibleManager()
    all_objects = models.Manager()


# Market taxonomy model
class Market(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = "Market"
        verbose_name_plural = "Markets"
        ordering = ["name"]
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False)
    description = models.TextField(help_text="Enter the market description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the market should be visible")
    image_sm = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_md = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_lg = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    visible_objects = VisibleManager()
    all_objects = models.Manager()


# MediaType taxonomy model
class MediaType(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = "Media Type"
        verbose_name_plural = "Media Types"
        ordering = ["name"]
        db_table = "portfolio_media_type"
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False)
    description = models.TextField(help_text="Enter the media type description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the media type should be visible")
    image_sm = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_md = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_lg = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    visible_objects = VisibleManager()
    all_objects = models.Manager()


# Role taxonomy model
class Role(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["name"]
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False)
    description = models.TextField(help_text="Enter the role description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the role should be visible")
    image_sm = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_md = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_lg = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    visible_objects = VisibleManager()
    all_objects = models.Manager()


# Project model
class Project(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["name"]
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False)
    description = models.TextField(help_text="Enter the project description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the project should be visible")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    visible_objects = VisibleManager()
    all_objects = models.Manager()

    def get_ordered_items(self):
        return self.items.filter(visible=True).order_by("item_order")

    def get_first_item(self):
        return self.items.filter(visible=True).order_by("item_order").first()

    def get_absolute_url(self):
        first_item = self.get_first_item()
        if first_item is not None:
            return first_item.get_absolute_url()
        else:
            return reverse('project_detail', kwargs={'slug': self.slug})


# ProjectItem model
class ProjectItem(TaxonomyMixin, models.Model):
    STATUS_CHOICES = [
        ("P", "Publish"),
        ("D", "Draft"),
        ("PR", "Private"),
        ("T", "Trash"),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="D")

    class Meta:
        verbose_name = "Project Item"
        verbose_name_plural = "Project Items"
        ordering = ["project"]
        db_table = "portfolio_project_item"
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="items", related_query_name="item")
    name = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(max_length=200, blank=False, null=False)
    description = models.TextField(help_text="Enter the project item description", blank=True, null=True)
    html_content = models.TextField(blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the project item should be visible")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="project_items", related_query_name="project_item", blank=True, null=True)
    industry = models.ManyToManyField(Industry, related_name="project_items", related_query_name="project_item", blank=True)
    market = models.ManyToManyField(Market, related_name="project_items", related_query_name="project_item", blank=True)
    media_type = models.ManyToManyField(MediaType, related_name="project_items", related_query_name="project_item", blank=True)
    role = models.ManyToManyField(Role, related_name="project_items", related_query_name="project_item", blank=True)
    year = models.IntegerField(help_text="Enter the project year as a 4-digit number", blank=True, null=True, validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)])
    item_order = models.IntegerField(help_text="Enter the project item order", blank=True, null=True, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    visible_objects = ProjectItemVisibleManager()
    all_objects = models.Manager()

    # Concatenate project name and project item name if they are different
    def get_project_and_item_name(self):
        if self.project.name == self.name:
            return self.name
        else:
            return f"{self.project.name} - {self.name}"

    # Generate the URL for the detail view of this project item
    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.slug)])

    # Override get_next and get_previous since don't have a project_item field
    def get_next(self):
        # Get the next item in the current project based on item_order
        next_item = self.project.items.filter(visible=True, item_order__gt=self.item_order).order_by('item_order').first()

        # If there is no next item in the current project, get the first item of the next project
        if next_item is None:

            # Get ALL projects that come after the current project as next_project before filtering down to one
            next_project = Project.visible_objects.annotate(lower_name=Lower('name')).filter(lower_name__gt=self.project.name.lower())

            # If there are no projects that come after the current project, get the first project in visible_objects
            if not next_project.exists():
                # Make sure next_project is always a QuerySet and not just a single Project object
                next_project = Project.visible_objects.filter(id=Project.visible_objects.first().id)

            # Get the first project that has:
            # - one visible project item
            # - client set to visible
            next_project = (
                next_project
                .annotate(
                    num_project_items=Count(
                        'item',
                        filter=Q(item__visible=True, item__client__visible=True)
                    )
                )
                .filter(num_project_items__gt=0)
                .first()
            )

            # If there is a next_project after filtering
            if next_project is not None:
                # Get the first visible project item in the next project
                for project_item in next_project.items.filter(visible=True).order_by('item_order'):
                    next_item = project_item
                    break

        return next_item

    def get_previous(self):
        # Get the previous item in the current project based on item_order
        previous_item = self.project.items.filter(visible=True, item_order__lt=self.item_order).order_by('-item_order').first()

        # If there is no previous item in the current project, get the last item of the previous project
        if previous_item is None:

            # Get ALL projects that come before the current project as previous_project before filtering down to one
            previous_project = Project.visible_objects.annotate(lower_name=Lower('name')).filter(lower_name__lt=self.project.name.lower()).order_by('lower_name')

            # If there are no projects that come before the current project, get the last project in visible_objects
            if not previous_project.exists():
                # Make sure next_project is always a QuerySet and not just a single Project object
                previous_project = Project.visible_objects.filter(id=Project.visible_objects.last().id)

            # Get the first previous project that has:
            # - one visible project item
            # - client set to visible
            previous_project = (
                previous_project
                .annotate(
                    num_project_items=Count(
                        'item',
                        filter=Q(item__visible=True, item__client__visible=True)
                    )
                )
                .filter(num_project_items__gt=0)
                .last()
            )

            # If there is a previous_project after filtering
            if previous_project is not None:
                # Get the last visible project item in the previous project
                for project_item in previous_project.items.filter(visible=True).order_by('item_order'):
                    previous_item = project_item
                    break

        return previous_item


class ProjectItemImage(models.Model):
    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        db_table = "portfolio_project_item_image"
    project_item = models.OneToOneField(ProjectItem, on_delete=models.CASCADE, related_name="image")
    original = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    medium = models.CharField(max_length=200)
    medium_large = models.CharField(max_length=200, blank=True, null=True)
    large = models.CharField(max_length=200, blank=True, null=True)
    admin_list_thumb = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProjectItemAttachment(models.Model):
    class Meta:
        verbose_name = "Project Attachment"
        verbose_name_plural = "Project Attachments"
        db_table = "portfolio_project_item_attachment"
    project_item = models.ForeignKey(ProjectItem, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="")
    description = models.TextField(blank=True, null=True)
    link_text = models.CharField(max_length=200)
    visible = models.BooleanField(default=True, help_text="Check if the project item attachment should be visible")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name
