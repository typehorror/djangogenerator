from django import template

from field.forms import NewModelFieldForm, FieldForm
from field.views import FIELD_FORMS

register = template.Library()

@register.inclusion_tag('new_model_field_form.html')
def new_model_field_form(model):
    form = NewModelFieldForm(prefix="new_field_%d" % model.id)
    return {'new_model_field_form': form, 'model': model}


@register.inclusion_tag('field_form.html')
def field_form(model_field):
    form = FIELD_FORMS[model_field.object.field_type](model=model_field.model, instance=model_field.object, prefix="%s_%d" % (model_field.object.field_type,model_field.id))
    return {'field_form':form,
            'model_field': model_field}
            

