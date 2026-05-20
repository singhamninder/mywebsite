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
            {
                "name": "Google Earth Engine",
                "icon_svg": "https://cdn.simpleicons.org/googleearthengine/4285F4",
                "label": "GEE",
            },
            {
                "name": "Apache Sedona",
                "icon_svg": "https://www.apache.org/logos/originals/sedona-2.svg",
                "label": "Sedona",
            },
            {
                "name": "Rasterio, Xarray, GeoPandas, Shapely",
                "icon_svg": "https://cdn.simpleicons.org/python/3776AB",
                "label": "Py",
            },
            {
                "name": "QGIS",
                "icon_svg": "https://cdn.simpleicons.org/qgis/589632",
                "label": "QGIS",
            },
            {
                "name": "Sentinel, Landsat, SAR",
                "label": "EO",
            },
        ],
    },
    {
        "name": "Machine Learning / Data",
        "items": [
            {
                "name": "Python - Pandas, Numpy",
                "icon_svg": "https://cdn.simpleicons.org/python/3776AB",
                "label": "Py",
            },
            {
                "name": "scikit-learn",
                "icon_svg": "https://cdn.simpleicons.org/scikitlearn/F7931E",
                "label": "SK",
            },
            {
                "name": "PyTorch",
                "icon_svg": "https://cdn.simpleicons.org/pytorch/EE4C2C",
                "label": "PT",
            },
            {
                "name": "TensorFlow",
                "icon_svg": "https://cdn.simpleicons.org/tensorflow/FF6F00",
                "label": "TF",
            },
        ],
    },
    {
        "name": "Cloud / MLOps",
        "items": [
            {
                "name": "Google Cloud - Vertex AI, Cloud Run, Cloud Storage",
                "icon_svg": "https://cdn.simpleicons.org/googlecloud/4285F4",
                "label": "GCP",
            },
            {
                "name": "AWS - S3, Lambda, Sagemaker",
                "icon_svg": "https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg",
                "label": "AWS",
            },
            {
                "name": "Apache Airflow",
                "icon_svg": "https://cdn.simpleicons.org/apacheairflow/017CEE",
                "label": "Airflow",
            },
            {
                "name": "MLflow",
                "icon_svg": "https://cdn.simpleicons.org/mlflow/0194E2",
                "label": "MLflow",
            },
            {
                "name": "Docker",
                "icon_svg": "https://cdn.simpleicons.org/docker/2496ED",
                "label": "DKR",
            },
            {
                "name": "GitHub Actions",
                "icon_svg": "https://cdn.simpleicons.org/githubactions/2088FF",
                "label": "GHA",
            },
            {
                "name": "Git",
                "icon_svg": "https://cdn.simpleicons.org/git/F05032",
                "label": "Git",
            },
        ],
    },
    {
        "name": "App / Web / Deployment",
        "items": [
            {
                "name": "Streamlit",
                "icon_svg": "https://cdn.simpleicons.org/streamlit/FF4B4B",
                "label": "ST",
            },
            {
                "name": "Django",
                "icon_svg": "https://cdn.simpleicons.org/django/092E20",
                "label": "DJ",
            },
            {
                "name": "FastAPI",
                "icon_svg": "https://cdn.simpleicons.org/fastapi/009688",
                "label": "FA",
            },
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
