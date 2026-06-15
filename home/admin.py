from django.contrib import admin

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
    )


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
    )

    # Allow multiple selection for tags
    filter_horizontal = ("tags",)

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


# Register all models
admin.site.register(Info, InfoAdmin)
admin.site.register(Skill)
admin.site.register(Work)
admin.site.register(Tag)
admin.site.register(Publication)
admin.site.register(Project, ProjectAdmin)
admin.site.register(RelatedPublication)
admin.site.register(TechStackGroup, TechStackGroupAdmin)
# admin.site.register(Contact)
