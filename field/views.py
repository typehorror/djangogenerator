from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.models import modelformset_factory


from common.shortcuts import render_response
from common.utils import paginate

from model.models import Model
from models import ModelField

from forms import *

FIELD_FORMS = {
    'charfield': CharFieldForm,
    'foreignkeyfield': ForeignKeyFieldForm,
    'manytomanyfield': ManyToManyFieldForm,
}

@login_required
@transaction.commit_manually
def model_field_del(request, model_field_id):
    if request.method == 'POST':
        model_field = get_object_or_404(ModelField, application__project__owner=request.user, pk=model_id)
        field = model_field.object
        #TODO: is it necessary to delete both or deleting object does it?
        try:
            model_field.delete()
            object.delete()
        except:
            transaction.rollback()
        else:
            transaction.commit()
        return HttpResponse("deleted")
    raise Http404

@login_required
def model_field_form(request, field_type, model_field_id):
    model_field = get_object_or_404(ModelField, model__application__project__owner=request.user, pk=model_field_id)
    context = {}
    if request.method == 'POST':
        form = FIELD_CHOICES[field_type](request.POST, prefix="%s_%d" % (field_type,model.id), instance=model_field.object)
        if form.is_valid():
            field = form.save()
            form = FIELD_CHOICES[field_type](instance=field, prefix="%s_%d" % (field_type,field.id))
    else:
        form = FIELD_CHOICES[field_type](instance=model_field.object,prefix="%s_%d" % (field_type,model_field.id))
    context = { 'form_field':form, 'model':model }
    return render_response(request, 'model_field_form.html', context)

@login_required
def new_model_field_form(request, field_type, model_id):
    if field_type not in FIELD_FORMS:
        raise Http404
    model = get_object_or_404(Model, application__project__owner=request.user, pk=model_id)
    context = {}
    if request.method == 'POST':
        form = FIELD_FORMS[field_type](request.POST, prefix="%s_%d" % (field_type,model.id))
        if form.is_valid():
            new_field = form.save()
            model.fields.add(new_field)
            form = FIELD_FORMS[field_type](instance=new_field, prefix="%s_%d" % (field_type,new_field.id))
            context = { 'field_form':form, 'model':model }
            return render_response(request, 'model_field_form.html', context)
    else:
        form = FIELD_FORMS[field_type](prefix="%s_%d" % (field_type,model.id))
    context = { 'new_field_form':form, 'model':model }
    return render_response(request, 'new_field_form.html', context)


#def new_model_field_form(request, model_id):
#    model = get_object_or_404(Model, application__project__owner=request.user, pk=model_id)
#    context = {}
#    if request.method == 'POST':
#        form = NewModelFieldForm(request.POST, prefix="new_field_%d" % model.id)
#        if form.is_valid():
#            context['created'] = True
#            context['field'] = 'test'
#    else:
#       form = NewModelFieldForm(request.POST, prefiex="new_field_%d" % model.id)
#    context.update({'new_model_field_form': form, 'model': model})
#    return render_response(request, 'new_model_field_form.html', context)
