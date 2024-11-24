from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import io
import matplotlib.pyplot as plt
from django.http import HttpResponse
from.models import Project, Achievement


def display_graph(request):
    # Generate a sample graph
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
    ax.set_title('Sample Graph')

    # Save graph to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')
def upload_project(request):
    if request.method == 'POST' and request.FILES['project_file']:
        project_file = request.FILES['project_file']
        fs = FileSystemStorage()
        filename = fs.save(project_file.name, project_file)
        file_url = fs.url(filename)
        return render(request, 'upload_project.html', {'file_url': file_url})
    return render(request, 'upload_project.html')

def index(request):
    return render(request, 'index.html', {'title': 'My Portfolio'})

def index(request):
    total_projects = Project.objects.count()
    return render(request, 'index.html', {'total_projects': total_projects})

def profile(request):
    achievements = Achievement.objects.all()
    total_projects = Project.objects.count()
    return render(request, 'profile.html', {
        'achievements': achievements,
        'total_projects': total_projects,
    })
    
def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})
