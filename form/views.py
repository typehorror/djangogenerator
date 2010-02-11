from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.models import modelformset_factory


from common.shortcuts import render_response
from common.utils import paginate

from model.models import Model
from models import ModelForm

from forms import *

@login_required
def model_form_form(request, model_form_id):
    """
    Allow update of a given ModelForm. 
    Current user must own the destination model.
    """
    model_form = get_object_or_404(ModelForm, pk=model_form_id, model__application__project__owner=request.user)
    context = {}
    prefix = "modelform_%d" % model_form.id
    if request.method == 'POST':
        form = ModelFormForm(model_form.model, request.POST, instance=model_form, prefix=prefix)
        if form.is_valid():
            model_form = form.save()
            form = ModelFormForm(model_form.model, request.POST, instance=model_form, prefix=prefix)
            context['saved'] = True
    else:
        form = ModelFormForm(model_form.model, instance=model_form, prefix=prefix)
    context.update({'model_form_form': form,
                    'model_form': model_form})
    return render_response(request, 'model_form_form.html', context)

@login_required
def model_form_del(request, model_form_id):
    if request.method == 'POST':
        model_form = get_object_or_404(ModelForm, model__application__project__owner=request.user, pk=model_form_id)
        model_form.delete()
        return HttpResponse("deleted")
    raise Http404


@login_required
def new_model_form_form(request, model_id):
    """
    Create a new ModelForm if the form is valid, otherwise display the
    initial form.
    Current user must own the destination model.
    If a new ModelForm is created, the template will use ajax to render it 
    and append it to the FormList.
    """
    model = get_object_or_404(Model, pk=model_id, application__project__owner=request.user)
    context = {}
    prefix = "new_modelform_%d" % model.id
    if request.method == 'POST':
        form = NewModelFormForm(model, request.POST, prefix=prefix)
        if form.is_valid():
            model_form = form.save(commit=False)
            model_form.model = model
            model_form.save()
            form = NewModelFormForm(model, prefix=prefix)
            context.update({'created': True,
                            'model_form': model_form})
    else:
       form = NewModelFormForm(model, request.POST, prefix=prefix)
    context.update({ 'new_model_form_form': form,
                     'model': model})
    return render_response(request, 'new_model_form_form.html', context)

@login_required
def model_form_view(request, model_form_id):
    model_form = get_object_or_404(ModelForm, model__application__project__owner=request.user, pk=model_form_id)
    return render_response(request, 'model_form_view.html', {'model_form':model_form})
