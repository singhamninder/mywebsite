from django.contrib import admin

from .models import Info, Skill, Project, Tag, Publication, Work, Contact

admin.site.register(Info)
admin.site.register(Skill)
admin.site.register(Work)
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Publication)
admin.site.register(Contact)