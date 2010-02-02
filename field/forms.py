from django import forms
from model.utils import slugify
from model.models import Model

from models import CharField, ForeignKeyField, ManyToManyField

FIELD_CHOICES = (
    ('charfield','CharField'),
    ('foreignkeyfield','ForeignKeyField'),
    ('manytomanyfield','ManyToManyField'),
)

class NewModelFieldForm(forms.Form):
    type = forms.ChoiceField(choices=FIELD_CHOICES)

class FieldForm(forms.ModelForm):
    def __init__(self, project, *args, **kwargs):
        super(FieldForm, self).__init__(*args, **kwargs)
        if 'relation' in self.fields:
            self.fields['relation'].queryset = Model.objects.filter(application__project=project)

class CharFieldForm(FieldForm):
    class Meta:
        model = CharField

class ManyToManyFieldForm(FieldForm):
    class Meta:
        model = ManyToManyField

class ForeignKeyFieldForm(FieldForm):
    class Meta:
        model = ForeignKeyField
