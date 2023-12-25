import datetime
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.db import models


class TaxonomyMixin(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def get_verbose_name(self):
        return self._meta.verbose_name

    def get_verbose_name_plural(self):
        return self._meta.verbose_name_plural

    def get_absolute_url(self):
        return reverse(f'{self._meta.model_name}_detail', args=[str(self.slug)])


# Client taxonomy model
class Client(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['name']
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(help_text="Enter the client description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the client should be visible")
    logo = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    website = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Industry taxonomy model
class Industry(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'
        ordering = ['name']
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(help_text="Enter the industry description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the industry should be visible")
    image_sm = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_md = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_lg = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Market taxonomy model
class Market(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = 'Market'
        verbose_name_plural = 'Markets'
        ordering = ['name']
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(help_text="Enter the market description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the market should be visible")
    image_sm = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_md = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_lg = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# MediaType taxonomy model
class MediaType(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = 'Media Type'
        verbose_name_plural = 'Media Types'
        ordering = ['name']
        db_table = 'portfolio_media_type'
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(help_text="Enter the media type description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the media type should be visible")
    image_sm = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_md = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_lg = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Role taxonomy model
class Role(TaxonomyMixin, models.Model):
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(help_text="Enter the role description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the role should be visible")
    image_sm = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_md = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    image_lg = models.URLField(max_length=200, blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Project model: Each project has a client, industry, market, media type, and role assigned to it
class Project(models.Model):
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['name']
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(help_text="Enter the project description", blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the project should be visible")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='projects', related_query_name='project', blank=True, null=True)
    industry = models.ManyToManyField(Industry, related_name='projects', related_query_name='project', blank=True)
    market = models.ManyToManyField(Market, related_name='projects', related_query_name='project', blank=True)
    mediatype = models.ManyToManyField(MediaType, related_name='projects', related_query_name='project', blank=True)
    role = models.ManyToManyField(Role, related_name='projects', related_query_name='project', blank=True)
    year = models.IntegerField(help_text="Enter the project year as a 4-digit number", blank=True, null=True, validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_verbose_name(self):
        return self._meta.verbose_name

    def get_verbose_name_plural(self):
        return self._meta.verbose_name_plural

    def get_ordered_items(self):
        return self.items.all().order_by('item_order')

    def get_first_item(self):
        return self.items.all().order_by('item_order').first()

    def get_absolute_url(self):
        return reverse('project', args=[str(self.slug)])


# ProjectItem model: Each project item has a project assigned to it
class ProjectItem(models.Model):
    STATUS_CHOICES = [
        ('P', 'Publish'),
        ('D', 'Draft'),
        ('PR', 'Private'),
        ('T', 'Trash'),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='D')

    class Meta:
        verbose_name = 'Project Item'
        verbose_name_plural = 'Project Items'
        ordering = ['project']
        db_table = 'portfolio_project_item'
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='items', related_query_name='item')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(help_text="Enter the project item description", blank=True, null=True)
    html_content = models.TextField(blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Check if the project item should be visible")
    item_order = models.IntegerField(help_text="Enter the project item order", blank=True, null=True, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_verbose_name(self):
        return self._meta.verbose_name

    def get_verbose_name_plural(self):
        return self._meta.verbose_name_plural

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.slug)])


class ProjectItemImage(models.Model):
    class Meta:
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'
        db_table = 'portfolio_project_item_image'
    project_item = models.OneToOneField(ProjectItem, on_delete=models.CASCADE, related_name='image')
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
        verbose_name = 'Project Attachment'
        verbose_name_plural = 'Project Attachments'
        db_table = 'portfolio_project_item_attachment'
    project_item = models.ForeignKey(ProjectItem, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='')
    description = models.TextField(blank=True, null=True)
    link_text = models.CharField(max_length=200)
    visible = models.BooleanField(default=True, help_text="Check if the project item attachment should be visible")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name
