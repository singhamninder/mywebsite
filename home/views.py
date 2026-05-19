from django.shortcuts import (
    # redirect,
    render,
)
from .models import (
    Info,
    Skill,
    Project,
    Publication,
    Work,
    # Contact,
)

# from django.contrib import messages

## for sending email and contact
# from django.core.mail import send_mail
# from django.conf import settings

TECH_STACK_GROUPS = [
    {
        "name": "Geospatial / Remote Sensing",
        "items": [
            {"name": "Google Earth Engine", "icon": "custom-gee", "label": "GEE"},
            {"name": "Apache Sedona", "icon": "custom-sedona", "label": "Sedona"},
            {
                "name": "Rasterio, Xarray, GeoPandas, Shapely",
                "icon": "devicon-python-plain",
            },
            {"name": "QGIS", "icon": "custom-qgis", "label": "QGIS"},
            {
                "name": "Sentinel, Landsat, SAR",
                "icon": "custom-satellite",
                "label": "EO",
            },
        ],
    },
    {
        "name": "Machine Learning / Data",
        "items": [
            {"name": "Python - Pandas, Numpy", "icon": "devicon-python-plain"},
            {"name": "scikit-learn", "icon": "devicon-scikitlearn-plain"},
            {"name": "PyTorch", "icon": "devicon-pytorch-original"},
            {"name": "TensorFlow", "icon": "devicon-tensorflow-original"},
        ],
    },
    {
        "name": "Cloud / MLOps",
        "items": [
            {
                "name": "Google Cloud - Vertex AI, Cloud Run, Cloud Storage",
                "icon": "devicon-googlecloud-plain",
            },
            {
                "name": "AWS - S3, Lambda, Sagemaker",
                "icon": "devicon-amazonwebservices-plain-wordmark",
            },
            {"name": "Docker", "icon": "devicon-docker-plain"},
            {"name": "GitHub Actions", "icon": "devicon-githubactions-plain"},
            {"name": "Git", "icon": "devicon-git-plain"},
        ],
    },
    {
        "name": "App / Web / Deployment",
        "items": [
            {"name": "Streamlit", "icon": "devicon-streamlit-plain"},
            {"name": "Django", "icon": "devicon-django-plain"},
            {"name": "FastAPI", "icon": "devicon-fastapi-plain"},
        ],
    },
]

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
    lworks = Work.objects.filter(
        title__in=[
            "Data Scientist",
            "Geospatial Data Scientist (Contract)",
            "Post-Doctoral Scholar",
        ]
    )
    rworks = Work.objects.exclude(
        title__in=[
            "Data Scientist",
            "Geospatial Data Scientist (Contract)",
            "Post-Doctoral Scholar",
        ]
    )
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
        "tech_stack_groups": TECH_STACK_GROUPS,
        "hero_rotating_phrases": HERO_ROTATING_PHRASES,
    }

    return render(request, "index.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, "single-project.html", {"project": projectObj})
