from django import forms
from django.core.exceptions import ValidationError

from model.utils import slugify

from models import ModelForm
from field.models import ModelField

class MyFieldMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, field):
        return field.object.name

class ModelFormForm(forms.ModelForm):
    def __init__(self, model, *args, **kwargs):
        super(ModelFormForm, self).__init__(*args, **kwargs)
        self.model = model
        # Here we want to limit the choices to the concerned model only
        if 'model_fields' in self.fields:
            self.fields['model_fields'] = MyFieldMultipleChoiceField(queryset = ModelField.objects.filter(model=model))

    def clean_name(self):
        """
        ensure that a name get cast to CamelCase
        "my model form name" should become "MyModelFormName"
        and that it is not already in use
        """
        name = self.cleaned_data["name"]
        name = ''.join([ '%s%s' % (x[0].upper(),x[1:]) for x in name.split(' ') if x ])
        name = slugify(name)

        if not (self.instance and self.instance.name == name ):
            if ModelForm.objects.filter(name=name, model__application=self.model.application):
               raise ValidationError('%s is already in used in this application' % name)

        return name

    class Meta:
        model = ModelForm
        fields = ('name',
                  'model_fields',)

class NewModelFormForm(ModelFormForm):
    class Meta:
        model = ModelForm
        fields = ('name',)

