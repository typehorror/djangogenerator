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
    'ForeignKey': ForeignKeyFieldForm,
    'ManyToManyField': ManyToManyFieldForm,
    'AutoField': AutoFieldForm,
    'BigIntegerField': BigIntegerFieldForm,
    'BooleanField': BooleanFieldForm,
    'CharField': CharFieldForm,
    'CommaSeparatedIntegerField': CommaSeparatedIntegerFieldForm,
    'DateField': DateFieldForm,
    'DateTimeField': DateTimeFieldForm,
    'DecimalField': DecimalFieldForm,
    'EmailField': EmailFieldForm,
    'FileField': FileFieldForm,
    'FilePathField': FilePathFieldForm,
    'FloatField': FloatFieldForm,
    'ImageField': ImageFieldForm,
    'IntegerField': IntegerFieldForm,
    'IPAddressField': IPAddressFieldForm,
    'NullBooleanField': NullBooleanFieldForm,
    'OneToOneField': OneToOneFieldForm,
    'PositiveIntegerField': PositiveIntegerFieldForm,
    'PositiveSmallIntegerField': PositiveSmallIntegerFieldForm,
    'SlugField': SlugFieldForm,
    'SmallIntegerField': SmallIntegerFieldForm,
    'TextField': TextFieldForm,
    'TimeField': TimeFieldForm,
    'URLField': URLFieldForm,
    'XMLField': XMLFieldForm,
}

@login_required
@transaction.commit_manually
def model_field_del(request, model_field_id):
    #FIXME: this should be event driven
    if request.method == 'POST':
        model_field = get_object_or_404(ModelField, model__application__project__owner=request.user, pk=model_field_id)
        field = model_field.object
        #TODO: is it necessary to delete both or deleting object does it?
        try:
            model_field.delete()
            field.delete()
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
    prefix = "%s_%d" % (model_field.object.field_type,model_field.id)
    if request.method == 'POST':
        form = FIELD_FORMS[model_field.object.field_type](model_field.model, request.POST, prefix=prefix, instance=model_field.object)
        if form.is_valid():
            field = form.save()
            form = FIELD_FORMS[model_field.object.field_type](model_field.model, instance=model_field.object, prefix=prefix)
            context['saved'] = True
    else:
        form = FIELD_FORMS[model_field.object.field_type](model_field.model, instance=model_field.object, prefix=prefix)
    context.update({'field_form':form, 
                    'model_field':model_field})
    return render_response(request, 'field_form.html', context)

@login_required
def new_model_field_form(request, field_type, model_id):
    if field_type not in FIELD_FORMS:
        raise Http404
    model = get_object_or_404(Model, application__project__owner=request.user, pk=model_id)
    context = {}
    prefix = "%s_%d" % (field_type,model.id)
    if request.method == 'POST':
        form = FIELD_FORMS[field_type](model, request.POST, prefix=prefix)
        if form.is_valid():
            new_field = form.save()
            model_field = model.model_fields.create(object=new_field)
            form = FIELD_FORMS[field_type](model, instance=new_field, prefix=prefix)
            context = { 'field_form':form, 
                        'model_field': model_field}
            return render_response(request, 'field_form.html', context)
    else:
        form = FIELD_FORMS[field_type](model, prefix=prefix)
    context = { 'new_field_form':form, 
                'model':model, 
                'field_type':field_type }
    return render_response(request, 'new_field_form.html', context)

