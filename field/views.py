from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.models import modelformset_factory


from common.shortcuts import render_response
from common.utils import paginate

from models import ModelField

@login_required
def model_field_view(request, model_field_id):
    model_fied = get_object_or_404(ModelField, model__application__project__owner=request.user, pk=model_field_id)
    return render_response(request, 'model_field_view.html', {'model_field':model_field})

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
def model_field_form(request, model_field_id):
    model_fied = get_object_or_404(ModelField, model__application__project__owner=request.user, pk=model_field_id)
    import pdb; pdb.set_trace()
    context = {}
    raise Http404

def new_model_field_form(request, model_id):
    model = get_object_or_404(Model, application__project__owner=request.user, pk=model_id)
    context = {}
    if request.method == 'POST':
        form = NewFieldForm(request.POST, prefiex="new_field_%d" % model_id)
        if form.is_valid():
            context['created'] = True
            context['field'] = 'test'
    else:
       form = NewFieldForm(request.POST, prefiex="new_field_%d" % model_id)
    context.update({'new_model_field_form': form, 'model': model})
    return render_response(request, 'new_model_field_form.html', context)
