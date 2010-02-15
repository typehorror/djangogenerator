from django import template

from model.forms import ModelForm, NewModelForm

register = template.Library()

@register.inclusion_tag('model_view.html')
def model_view(model):
    return {'model':model}

@register.inclusion_tag('model_form.html')
def model_form(model):
    form = ModelForm(instance=model, prefix="model_%d_" % model.id)
    return {'model_form': form, 'model': model}

@register.inclusion_tag('new_model_form.html')
def new_model_form(application):
    form = NewModelForm(application=application, prefix="new_model_%d" % application.id)
    return {'new_model_form': form, 'application': application}

