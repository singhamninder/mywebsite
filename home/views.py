from django.shortcuts import render
from .models import Info, Skill, Project, Publication, Work

## for sending email and contact
# from .forms import ContactForm
# from django.core.mail import send_mail
# from django.core.checks import messages
# from django.conf import settings


def home(request):
    infos = Info.objects.all()
    skills = Skill.objects.exclude(description__exact="")
    otherskills = Skill.objects.filter(description="")
    works = Work.objects.all()
    projects = Project.objects.all()
    publications = Publication.objects.all()

    # form = ContactForm()
    # if request.method == 'POST':
    #     form = ContactForm(request.POST)
    #     if form.is_valid():

    context = {
        'infos':infos,
        'skills':skills,'otherskills':otherskills,
        'works':works,
        'projects':projects,
        'publications':publications,
        # 'form':form,
    }

    return render(request, 'index.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'single-project.html', {'project': projectObj})

