from math import ceil

from django.shortcuts import (
    # redirect,
    render,
)
from .models import (
    Info,
    Skill,
    Project,
    Publication,
    TechStackGroup,
    Work,
    # Contact,
)

# from django.contrib import messages

## for sending email and contact
# from django.core.mail import send_mail
# from django.conf import settings

HERO_ROTATING_PHRASES = [
    "AI/ML pipelines",
    "remote sensing workflows",
    "Earth observation tools",
    "landcover classification systems",
]


def home(request):
    infos = Info.objects.all()
    skills = Skill.objects.exclude(description__exact="")
    otherskills = Skill.objects.filter(description="")
    works = list(Work.objects.all())
    mid = ceil(len(works) / 2)
    lworks, rworks = works[:mid], works[mid:]
    projects = Project.objects.all()
    featured_projects = projects.filter(featured=True)
    if not featured_projects.exists():
        featured_projects = projects[:6]
    publications = Publication.objects.all()

    # if request.method == 'POST':
    #     contact = Contact()

    #     contactName=request.POST.get('contactName')
    #     contactEmail=request.POST.get('contactEmail')
    #     contactSubject=request.POST.get('contactSubject')
    #     contactMessage=request.POST.get('contactMessage')

    #     contact.contactName=contactName
    #     contact.contactEmail=contactEmail
    #     contact.contactSubject=contactSubject
    #     contact.contactMessage=contactMessage
    #     contact.save()
    #     messages.success(request, 'Your message was sent, thank you!')

    #     return redirect('home')

    context = {
        "infos": infos,
        "skills": skills,
        "otherskills": otherskills,
        "lworks": lworks,
        "rworks": rworks,
        "projects": projects,
        "featured_projects": featured_projects,
        "publications": publications,
        "tech_stack_groups": TechStackGroup.objects.prefetch_related("items"),
        "hero_rotating_phrases": HERO_ROTATING_PHRASES,
    }

    return render(request, "index.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    info = Info.objects.first()
    return render(request, "single-project.html", {"project": projectObj, "info": info})
