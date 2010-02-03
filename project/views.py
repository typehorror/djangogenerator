import os
from tempfile import mktemp

from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings

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


def generate(template, output, context={}):
    content = render_to_string(template, context)
    try:
        file = open(output, 'w+')
    except IOError:
        import pdb; pdb.set_trace()
    file.write(content)
    file.close()

@login_required
def project_generate(request, project_id):
    project = get_object_or_404(Project, owner=request.user, pk=project_id)
    context = {'project': project}
    
    # make the output folder
    output_folder = mktemp()
    os.mkdir(output_folder)

    # generate the url file and save it
    generate('urls.py', os.path.join(output_folder, 'urls.py'), context)


    # generate the settings(_local) files and save them
    generate('settings.py', os.path.join(output_folder, 'settings.py'), context)
    generate('settings_local.py', os.path.join(output_folder, 'settings_local.py'), context)

    for application in project.applications.all():
        context = {'application': application}
        application_folder = os.path.join(output_folder, application.name)
        templates_folder = os.path.join(output_folder, '%s/templates' % application.name)

        # generate the application folder
        os.mkdir(application_folder)

        # genereate the templates folder
        os.mkdir(templates_folder)

        # generate models
        generate('application/models.py', os.path.join(application_folder, 'models.py'), context)

        # generate views
        generate('application/views.py', os.path.join(application_folder, 'views.py'), context)

        # generate forms
        generate('application/forms.py', os.path.join(application_folder, 'forms.py'), context)

        # generate urls
        generate('application/urls.py', os.path.join(application_folder, 'urls.py'), context)
        
        # generate admin
        generate('application/admin.py', os.path.join(application_folder, 'admin.py'), context)
        
        # generate __init__
        generate('application/__init__.py', os.path.join(application_folder, '__init__.py'), context)
        
        for model in application.models.all():
            context.update({'model': model})

            # generate the read only view
            if model.has_read_only_view:
                generate('application/templates/view.html', open(templates_folder, '%s_view.html' % model.name.lower()), context)

            # generate the form view
            if model.has_form_view:
                generate('application/templates/form.html', open(templates_folder, '%s_form.html' % model.name.lower()), context)

    tgz_filename = '%d_%d.tgz' % (project.id, project.owner.id)
    os.system('cd %s && tar czf %s * && mv %s %s ' % (output_folder, tgz_filename, tgz_filename, settings.STATIC_ROOT))
    return HttpResponseRedirect('%s%s' % (settings.STATIC_URL, tgz_filename))
