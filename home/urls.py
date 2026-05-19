from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("project/<int:pk>/", views.project, name="project"),
    # path('submit/', views.submmit, name = "submit")
]
