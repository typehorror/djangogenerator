from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from common.shortcuts import render_response
from common.utils import paginate

from models import Application
from forms import ApplicationForm, NewApplicationForm
from project.models import Project

@login_required
def application_view(request, application_id):
    application = get_object_or_404(Application, project__owner=request.user, pk=application_id)
    context = {'application': application}
    return render_response(request, 'application_view.html', context)

@login_required
def application_del(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(Application, project__owner=request.user, pk=application_id)
        application.delete()
        return HttpResponse("deleted")
    raise Http404


@login_required
def application_form(request, application_id):
    application = get_object_or_404(Application, project__owner=request.user, pk=application_id)
    context = {}
    if request.method == "POST":
        form = ApplicationForm(application.project, request.POST, instance=application, prefix='app_%d_' % application.id)
        if form.is_valid():
            application = form.save()
            context['saved'] = True
            form = ApplicationForm(application.project, instance=application, prefix='app_%d_' % application.id)
    else:
        form = ApplicationForm(application.project, instance=application, prefix='app_%d_' % application.id)
    context.update({'application_form': form,
                    'application': application})
    return render_response(request, 'application_form.html', context)
    

@login_required
def new_application_form(request, project_id):
    project = get_object_or_404(Project, owner=request.user, pk=project_id)
    context = {}
    if request.method == 'POST':
        form = NewApplicationForm(project, request.POST, prefix="new_application_")
        if form.is_valid():
            context['created'] = True
            new_application = form.save(commit=False)
            new_application.project = project
            new_application.save()
            context['application'] = new_application
            form = NewApplicationForm(project, prefix="new_application_")
    else:
        form = NewApplicationForm(project, prefix="new_application_")
    context.update({'new_application_form': form, 'project': project})
    return render_response(request, 'new_application_form.html', context)

