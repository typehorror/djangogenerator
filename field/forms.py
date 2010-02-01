from django import forms
from model.utils import slugify

FIELD_CHOICES = (
    ('charfield','CharField'),
    ('foreignkeyfield','ForeignKeyField'),
    ('manytomanyfiekd','ManyToManyField'),
)

class NewFieldForm(forms.Form):
    type = forms.ChoiceField(choices=FIELD_CHOICES)
