from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from common.shortcuts import render_response
from common.utils import paginate

from models import Model
from forms import NewModelForm, ModelForm
from application.models import Application

@login_required
def model_view(request, model_id):
    model = get_object_or_404(Model, application__project__owner=request.user, pk=model_id)
    return render_response(request, 'model_view.html', {'model':model})

@login_required
def model_del(request, model_id):
    if request.method == 'POST':
        model = get_object_or_404(Model, application__project__owner=request.user, pk=model_id)
        model.delete()
        return HttpResponse("deleted")
    raise Http404

@login_required
def model_form(request, model_id):
    model = get_object_or_404(Model, application__project__owner=request.user, pk=model_id)
    context = {}
    if request.method == 'POST':
        model_form = ModelForm(request.POST, instance=model, prefix="model_%d_" % model.id)
        if model_form.is_valid():
            model = model_form.save()
            context['saved'] = True
            model_form = ModelForm(instance=model, prefix="model_%d_" % model.id)
        context.update({'model_form': model_form,
                        'model': model})
        return render_response(request, 'model_form.html', context)
    raise Http404

@login_required
def new_model_form(request, application_id):
    """
    Create a new model inside an application.
    return 404 if 
    """
    application = get_object_or_404(Application, project__owner=request.user, pk=application_id)
    context = {}
    if request.method == 'POST':
        form = NewModelForm(request.POST, application=application, prefix="new_model_%d" % application.id)
        if form.is_valid():
            context['created'] = True
            new_model = form.save(commit=False)
            new_model.application = application
            new_model.save()
            context['model']=new_model
            form = NewModelForm(application=application, prefix="new_model_%d" % application.id)
    else:
        form = NewModelForm(application=application, prefix="new_model_%d" % application.id)
    context.update({'new_model_form': form, 'application': application})
    return render_response(request, 'new_model_form.html', context)

