from django.shortcuts import redirect, render
from .models import Info, Skill, Project, Publication, Work, Contact
from django.contrib import messages

## for sending email and contact
# from django.core.mail import send_mail
# from django.conf import settings

def home(request):
    infos = Info.objects.all()
    skills = Skill.objects.exclude(description__exact="")
    otherskills = Skill.objects.filter(description="")
    lworks = Work.objects.filter(title__in=["Data Scientist", "Geospatial Data Scientist (Contract)", "Post-Doctoral Scholar"])
    rworks = Work.objects.exclude(title__in=["Data Scientist", "Geospatial Data Scientist (Contract)", "Post-Doctoral Scholar"])
    projects = Project.objects.all()
    publications = Publication.objects.all()

    if request.method == 'POST':
        contact = Contact()

        contactName=request.POST.get('contactName')
        contactEmail=request.POST.get('contactEmail')
        contactSubject=request.POST.get('contactSubject')
        contactMessage=request.POST.get('contactMessage')

        contact.contactName=contactName
        contact.contactEmail=contactEmail
        contact.contactSubject=contactSubject
        contact.contactMessage=contactMessage
        contact.save()
        messages.success(request, 'Your message was sent, thank you!')

        return redirect('home')

    context = {
        'infos':infos,
        'skills':skills,'otherskills':otherskills,
        'lworks':lworks,'rworks':rworks,
        'projects':projects,
        'publications':publications,
    }

    return render(request, 'index.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'single-project.html', {'project': projectObj})

