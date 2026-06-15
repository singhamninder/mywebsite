from io import StringIO

from django.contrib import admin, messages
from django.core.management import call_command
from django.shortcuts import redirect
from django.urls import path

from .models import (
    Info,
    Skill,
    Project,
    Tag,
    Publication,
    Work,
    RelatedPublication,
    TechStackGroup,
    TechStackItem,
)


class InfoAdmin(admin.ModelAdmin):
    fields = (
        "cv",
        "mainImage",
        "profile_image",
        "short_intro",
        "linkedin",
        "google_scholar",
        "github",
        "email",
        "orcid",
        "openalex_author_id",
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["orcid"].help_text = (
            "Optional ORCID id (e.g. 0000-0002-1825-0097). "
            "Used to resolve your OpenAlex author id when openalex_author_id is empty."
        )
        form.base_fields["openalex_author_id"].help_text = (
            'OpenAlex author id (e.g. "A5023888391"). '
            "Find it at openalex.org (Authors tab) or via "
            "https://api.openalex.org/authors/orcid:<your-orcid>"
        )
        return form


# Inline admin for related publications
class RelatedPublicationInline(admin.TabularInline):
    """
    Allows editing related publications directly from the Project admin page.
    TabularInline displays related publications in a compact table format.
    """

    model = RelatedPublication
    extra = 1  # Show 1 empty related publication form by default
    fields = ("title", "url")
    verbose_name = "Related publication"
    verbose_name_plural = "Related publications"


# Updated Project admin with related publications inline
class ProjectAdmin(admin.ModelAdmin):
    """
    Enhanced Project admin with inline related publications management
    """

    # Fields to display in the project list
    list_display = ("title", "featured", "created", "get_related_publication_count")

    # Fields to filter by in the admin sidebar
    list_filter = ("featured", "created", "tags")

    # Fields to search by
    search_fields = ("title", "description")

    # Fields to display when editing a project
    fields = (
        "title",
        "impact_summary",
        "description",
        "featured_image",
        "image1",
        "image2",
        "image3",
        "code_url",
        "demo_url",
        "featured",
        "tags",
        "publications",
    )

    # Allow multiple selection for tags and linked publications
    filter_horizontal = ("tags", "publications")

    # Include the related publications inline
    inlines = [RelatedPublicationInline]

    def get_related_publication_count(self, obj):
        """Display the number of related publications for each project in the list view."""
        return obj.related_publications.count()

    get_related_publication_count.short_description = "Related publications"


class TechStackItemInline(admin.TabularInline):
    model = TechStackItem
    extra = 1
    fields = ("name", "icon_url", "label", "order")


class TechStackGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    inlines = [TechStackItemInline]


class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "venue", "source")
    list_filter = ("source", "year")
    search_fields = ("title", "authors", "doi")
    change_list_template = "admin/home/publication/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync/",
                self.admin_site.admin_view(self.sync_publications_view),
                name="home_publication_sync",
            ),
        ]
        return custom_urls + urls

    def sync_publications_view(self, request):
        if request.method != "POST":
            return redirect("admin:home_publication_changelist")

        stdout = StringIO()
        try:
            call_command("sync_publications", stdout=stdout)
            summary = stdout.getvalue().strip()
            messages.success(request, f"Publications synced from OpenAlex: {summary}")
        except Exception as exc:
            messages.error(request, f"Sync failed: {exc}")

        return redirect("admin:home_publication_changelist")


# Register all models
admin.site.register(Info, InfoAdmin)
admin.site.register(Skill)
admin.site.register(Work)
admin.site.register(Tag)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(RelatedPublication)
admin.site.register(TechStackGroup, TechStackGroupAdmin)
# admin.site.register(Contact)
