from django.contrib import admin
from import_export import resources
from import_export.fields import Field
from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import ManyToManyWidget
from .models import Industry, Technology, Project, Company
from .forms import CustomImportForm, CustomConfirmImportForm


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    list_per_page = 25


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    list_per_page = 25


class ProjectResource(resources.ModelResource):
    def __init__(self, author=None):
        super().__init__()
        self.author = author

    url_is_active = Field(attribute='url_is_active', column_name='notes')
    technologies = Field(attribute='technologies', column_name='technologies',
                         widget=ManyToManyWidget(model=Technology, separator=', ', field='title'))
    industries = Field(attribute='industries', column_name='industries',
                       widget=ManyToManyWidget(model=Industry, separator=', ', field='title'))

    class Meta:
        model = Project
        fields = ('title', 'url', 'technologies', 'description', 'industries', 'url_is_active')
        export_order = ('title', 'url', 'technologies', 'description', 'industries', 'url_is_active')

    def dehydrate_url_is_active(self, project):
        """Processing field `url_is_active` on export"""
        if project.url_is_active:
            return ''
        return 'Doesn\'t work'

    def before_import_row(self, row, row_number=None, **kwargs):
        technologies = row.get('technologies')
        industries = row.get('industries')
        # Extract technologies' and industries' names from row
        technologies = [value.strip().capitalize() for value in technologies.split(',') if value]
        industries = [value.strip().capitalize() for value in industries.split(',') if value]

        # Change row immediately(capitalize each industry and technology) in order if pass row to the next
        # method, to be able to update project's strange written industries and technologies like 'PYTHON', 'jS'
        row['technologies'] = ", ".join(technologies)
        row['industries'] = ", ".join(industries)

        # Create technologies and industries if not exist yet
        for item in technologies:
            Technology.objects.get_or_create(title=item)
        for item in industries:
            Industry.objects.get_or_create(title=item)

        # Transform notes to boolean. If there is nothing in notes, `url_is_active` set to True
        row['notes'] = not row['notes']

    def get_instance(self, instance_loader, row):
        return Project.objects.filter(title=row.get('title'), author_id=self.author).first()

    def init_instance(self, row=None):
        instance = super().init_instance(row)
        instance.author_id = self.author
        return instance


@admin.register(Project)
class ProjectAdmin(ImportExportActionModelAdmin):
    resource_class = ProjectResource

    list_display = ("id", "title", "author", "url", "url_is_active", "is_private", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("author", "url_is_active", "created_at")
    raw_id_fields = ("industries", "technologies")
    search_fields = ("title", "description")
    list_per_page = 25

    def get_import_form(self):
        return CustomImportForm

    def get_confirm_import_form(self):
        return CustomConfirmImportForm

    def get_form_kwargs(self, form, *args, **kwargs):
        # pass `author` to the kwargs for initial state of the custom confirm form
        if isinstance(form, CustomImportForm):
            if form.is_valid():
                author = form.cleaned_data['author']
                kwargs.update({'author': author.id})
        return kwargs

    def get_resource_kwargs(self, request, *args, **kwargs):
        # On import add `author` to Resource's fields in order to be able to create new projects with a specific author
        rk = {}
        if form := kwargs.get('form'):  # there is no form for exporting data
            if form.is_valid():
                author = form.cleaned_data['author']
                rk.update({'author': author.id})
        return rk


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "founder", "website", "email", "slogan")
    list_display_links = ("id", "name")
    search_fields = ("name", "description", "founder", "email", "slogan")
    list_per_page = 25
