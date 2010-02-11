from django import template

from form.forms import ModelFormForm, NewModelFormForm

register = template.Library()

@register.inclusion_tag('model_form_form.html')
def model_form_form(model_form):
    prefix = "modelform_%d" % model_form.id
    form = ModelFormForm(model_form.model, instance=model_form, prefix=prefix)
    return {'model_form_form': form, 'model_form': model_form}


@register.inclusion_tag('new_model_form_form.html')
def new_model_form_form(model):
    prefix = "new_modelform_%d" % model.id
    form = NewModelFormForm(model, prefix=prefix)
    return {'new_model_form_form': form, 'model': model}

@register.inclusion_tag('model_form_view.html')
def model_form_view(model_form):
    return {'model_form': model_form}
