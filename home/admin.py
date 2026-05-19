from django.contrib import admin

from .models import Info, Skill, Project, Tag, Publication, Work, Reference


class InfoAdmin(admin.ModelAdmin):
    fields = ("cv", "mainImage", "profile_image", "short_intro", "linkedin", "twitter")


# Inline admin for References
class ReferenceInline(admin.TabularInline):
    """
    Allows editing references directly from the Project admin page.
    TabularInline displays references in a compact table format.
    """

    model = Reference
    extra = 1  # Show 1 empty reference form by default
    fields = ("title", "url")
    verbose_name = "Reference"
    verbose_name_plural = "References"


# Updated Project admin with References inline
class ProjectAdmin(admin.ModelAdmin):
    """
    Enhanced Project admin with inline References management
    """

    # Fields to display in the project list
    list_display = ("title", "featured", "created", "get_reference_count")

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
        "project_link",
        "publication_link",
        "featured",
        "tags",
    )

    # Allow multiple selection for tags
    filter_horizontal = ("tags",)

    # Include the References inline
    inlines = [ReferenceInline]

    def get_reference_count(self, obj):
        """Display the number of references for each project in the list view"""
        return obj.references.count()

    get_reference_count.short_description = "References"


# Register all models
admin.site.register(Info, InfoAdmin)
admin.site.register(Skill)
admin.site.register(Work)
admin.site.register(Tag)
admin.site.register(Publication)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Reference)
# admin.site.register(Contact)
