from django import template

from field.forms import NewModelFieldForm

register = template.Library()

@register.inclusion_tag('new_model_field_form.html')
def new_model_field_form(model):
    form = NewModelFieldForm(prefix="new_field_%d" % model.id)
    return {'new_model_field_form': form, 'model': model}
