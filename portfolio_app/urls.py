from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('upload_project/', views.upload_project, name='upload_project'),  # Upload project
    path('display_graph/', views.display_graph, name='display_graph'),  # Display graph route
    path('profile/', views.profile, name='profile'),
    path('projects/', views.projects, name='projects'),
]
