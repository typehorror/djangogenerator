import os
from tempfile import mktemp

from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from common.shortcuts import render_response
from common.utils import paginate

from models import Project
from forms import NewProjectForm, ProjectForm
from application.forms import NewApplicationForm

from field.models import ModelField

def public_project_view(request, project_id):
    """
    - return project corresponding to project_id
    - raise 404 if project is not found or is not public
    """
    if request.user.is_superuser:
        project = get_object_or_404(Project, pk=project_id)
    else:
        project = get_object_or_404(Project, public=True, pk=project_id)
    
    context = {'project': project}
    return render_response(request, 'project/public_project_view.html', context)

def public_project_list(request):
    """
    return public projects list
    The result list is paginated
    """
    context = {}
    projects = Project.objects.filter(public=True).order_by("-creation_date")
    context['projects'] = paginate(projects, request)
    return render_response(request, 'project/public_project_list.html', context) 

@login_required
def project_view(request, project_id):
    """
    - return project corresponding to project_id
    - handle project modification form submition
    - raise 404 if project is not found or project doesn't belong to the current user
    """
    if request.user.is_superuser:
        project = get_object_or_404(Project, pk=project_id)
    else:
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
def project_del(request, project_id):
    """
    Delete a project
    raise 404 if project doesn't exist or user is not project's owner
    """
    project = get_object_or_404(Project, owner=request.user, pk=project_id)
    project.delete()
    return HttpResponse("deleted")

@login_required
def project_list(request):
    """
    return projects own by the current user.
    The result list is paginated
    """
    context = {}
    projects = Project.objects.filter(owner=request.user).order_by("-creation_date")
    if request.method == "POST":
        form = NewProjectForm(request.POST, owner=request.user)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()
    else:
        form = NewProjectForm(owner=request.user)
    context['projects'] = paginate(projects, request)
    context['new_project_form'] = form
    return render_response(request, 'project/project_list.html', context) 

def generate(template, output, context={}):
    """
    render a template to a file using context dict
    """
    content = render_to_string(template, context)
    try:
        file = open(output, 'w+')
    except IOError:
        import pdb; pdb.set_trace()
    file.write(content.encode('utf-8'))
    file.close()

@login_required
def project_generate(request, project_id):
    return _project_generate(request=request, project_id=project_id, owner=request.user)

def public_project_generate(request, project_id):
    return _project_generate(request=request, project_id=project_id)

def _project_generate(request, project_id, owner=None):
    """
    Generate the whole project in a temp folder,
    compress it and move the compressed file to media folder.
    """
    project_kwargs = {'pk':project_id}
    if owner:
        project_kwargs['owner'] = owner
    else:
         project_kwargs['public'] = True
    project = get_object_or_404(Project, **project_kwargs)
    context = {'project': project}
    
    # make the output folder
    output_folder = mktemp()
    os.mkdir(output_folder)

    # generate the url file and save it
    generate('urls.py', os.path.join(output_folder, 'urls.py'), context)

    # generate __init__ file
    generate('__init__.py', os.path.join(output_folder, '__init__.py'), context)


    # generate the settings(_local) files and save them
    generate('settings.py', os.path.join(output_folder, 'settings.py'), context)

    # generate the manage.py file
    generate('manage.py', os.path.join(output_folder, 'manage.py'), context)
    os.chmod(os.path.join(output_folder, 'manage.py'), 0744)

    #generate base template
    templates_folder = os.path.join(output_folder, 'templates')
    os.mkdir(templates_folder)
    generate('templates/base.html', os.path.join(templates_folder, 'base.html'), context)
    generate('templates/homepage.html', os.path.join(templates_folder, 'homepage.html'), context)

    # generate registration templates if necessary
    registration_folder = os.path.join(templates_folder, 'registration')
    os.mkdir(registration_folder)
    registration_templates = ['login.html', 
                              'password_change_done.html', 
                              'password_change_form.html', 
                              'password_reset_complete.html', 
                              'password_reset_confirm.html',
                              'password_reset_done.html',
                              'password_reset_email.html',
                              'password_reset_form.html',]
    for filename in registration_templates:
        generate('templates/registration/%s' % filename, os.path.join(registration_folder, filename), context)

    # generate media
    media_folder = os.path.join(output_folder, 'media')
    os.mkdir(media_folder)
    css_folder = os.path.join(media_folder, 'css')
    os.mkdir(css_folder)
    css_files = ['screen.css',
                 'ie6.css',
                 'reset.css',
                 'print.css']
    for filename in css_files:
        generate('media/css/%s' % filename, os.path.join(css_folder, filename), context)

    for application in project.applications.all():
        # make sure we don't generate empty models
        if not ModelField.objects.filter(model__application=application):
            continue
        context.update({'application': application})
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
            # make sure we don't generate empty models
            if not model.model_fields.all():
                continue
            context.update({'model': model})

            # generate the read only view
            if model.has_read_only_view:
                generate('application/templates/view.html', os.path.join(templates_folder, '%s_view.html' % model.name.lower()), context)

            # generate the form view
            if model.has_form_view:
                generate('application/templates/form.html', os.path.join(templates_folder, '%s_form.html' % model.name.lower()), context)

            if model.has_read_only_view or model.has_form_view:
                generate('application/templates/list.html', os.path.join(templates_folder, '%s_list.html' % model.name.lower()), context)
                generate('application/templates/base.html', os.path.join(templates_folder, '%s_base.html' % model.name.lower()), context)

    tgz_filename = '%d_%d.tgz' % (project.id, project.owner.id)
    #TODO: clean the temp folder using cron
    os.system('cd %s && tar czf %s * && mv %s %s ' % (output_folder, tgz_filename, tgz_filename, settings.MEDIA_ROOT))
    return HttpResponseRedirect('%s%s' % (settings.MEDIA_URL, tgz_filename))
