from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from common.shortcuts import render_response
from common.utils import paginate

from models import Project
from forms import NewProjectForm, ProjectForm
from application.forms import NewApplicationForm

@login_required
def project_view(request, project_id):
    project = get_object_or_404(Project, owner=request.user, pk=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
    else:
        form = ProjectForm(instance=project)
    
    context = {'project': project,
               'new_application_form': NewApplicationForm({'project_id':project.id}, prefix='new_application'),
               'project_form': form}
    return render_response(request, 'project/project_view.html', context)

@login_required
def project_list(request):
    context = {}
    projects = Project.objects.filter(owner=request.user)
    if request.method == "POST":
        form = NewProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()
    else:
        form = NewProjectForm()
    context['projects'] = paginate(projects, request)
    context['new_project_form'] = form
    return render_response(request, 'project/project_list.html', context) 
