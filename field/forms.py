from django import forms
from model.utils import slugify

FIELD_CHOICES = (
    ('charfield','CharField'),
    ('foreignkeyfield','ForeignKeyField'),
    ('manytomanyfield','ManyToManyField'),
)

class NewFieldForm(forms.Form):
    type = forms.ChoiceField(choices=FIELD_CHOICES)
