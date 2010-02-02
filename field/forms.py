from django import forms
from model.utils import slugify

from models import CharField, ForeignKeyField, ManyToManyField

FIELD_CHOICES = (
    ('charfield','CharField'),
    ('foreignkeyfield','ForeignKeyField'),
    ('manytomanyfield','ManyToManyField'),
)

class NewModelFieldForm(forms.Form):
    type = forms.ChoiceField(choices=FIELD_CHOICES)

class CharFieldForm(forms.ModelForm):
    class Meta:
        model = CharField

class ManyToManyFieldForm(forms.ModelForm):
    class Meta:
        model = ManyToManyField

class ForeignKeyFieldForm(forms.ModelForm):
    class Meta:
        model = ForeignKeyField
