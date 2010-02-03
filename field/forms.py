from django import forms
from model.utils import slugify
from model.models import Model

from models import *

FIELD_CHOICES = (
    ('AutoField', 'AutoField'),
    ('BigIntegerField', 'BigIntegerField'),
    ('BooleanField', 'BooleanField'),
    ('CharField', 'CharField'),
    ('CommaSeparatedIntegerField', 'CommaSeparatedIntegerField'),
    ('DateField', 'DateField'),
    ('DateTimeField', 'DateTimeField'),
    ('DecimalField', 'DecimalField'),
    ('EmailField', 'EmailField'),
    ('FileField', 'FileField'),
    ('FilePathField', 'FilePathField'),
    ('FloatField', 'FloatField'),
    ('ForeignKeyField','ForeignKeyField'),
    ('ImageField', 'ImageField'),
    ('IntegerField', 'IntegerField'),
    ('IPAddressField', 'IPAddressField'),
    ('ManyToManyField','ManyToManyField'),
    ('NullBooleanField', 'NullBooleanField'),
    ('PositiveIntegerField', 'PositiveIntegerField'),
    ('PositiveSmallIntegerField', 'PositiveSmallIntegerField'),
    ('SlugField', 'SlugField'),
    ('SmallIntegerField', 'SmallIntegerField'),
    ('TextField', 'TextField'),
    ('TimeField', 'TimeField'),
    ('URLField', 'URLField'),
    ('XMLField', 'XMLField'),
)

class NewModelFieldForm(forms.Form):
    type = forms.ChoiceField(choices=FIELD_CHOICES)

class FieldForm(forms.ModelForm):
    def __init__(self, project, *args, **kwargs):
        super(FieldForm, self).__init__(*args, **kwargs)
        if 'relation' in self.fields:
            self.fields['relation'].queryset = Model.objects.filter(application__project=project)

    def clean_name(self):
        name = self.cleaned_data["name"]
        name = slugify(name).lower()
        return name

class TextFieldForm(FieldForm):
    class Meta:
        model = TextField

class CharFieldForm(FieldForm):
    class Meta:
        model = CharField

class ManyToManyFieldForm(FieldForm):
    class Meta:
        model = ManyToManyField

class ForeignKeyFieldForm(FieldForm):
    class Meta:
        model = ForeignKeyField

class AutoFieldForm(FieldForm):
    class Meta:
        model = AutoField

class BigIntegerFieldForm(FieldForm):
    class Meta:
        model = BigIntegerField

class BooleanFieldForm(FieldForm):
    class Meta:
        model = BooleanField

class CommaSeparatedIntegerFieldForm(FieldForm):
    class Meta:
        model = CommaSeparatedIntegerField

class DateFieldForm(FieldForm):
    class Meta:
        model = DateField

class DateTimeFieldForm(FieldForm):
    class Meta:
        model = DateTimeField

class DecimalFieldForm(FieldForm):
    class Meta:
        model = DecimalField

class EmailFieldForm(FieldForm):
    class Meta:
        model = EmailField

class FileFieldForm(FieldForm):
    class Meta:
        model = FileField

class FilePathFieldForm(FieldForm):
    class Meta:
        model = FilePathField

class FloatFieldForm(FieldForm):
    class Meta:
        model = FloatField

class ImageFieldForm(FieldForm):
    class Meta:
        model = ImageField

class IntegerFieldForm(FieldForm):
    class Meta:
        model = IntegerField

class IPAddressFieldForm(FieldForm):
    class Meta:
        model = IPAddressField

class NullBooleanFieldForm(FieldForm):
    class Meta:
        model = NullBooleanField

class PositiveIntegerFieldForm(FieldForm):
    class Meta:
        model = PositiveIntegerField

class PositiveSmallIntegerFieldForm(FieldForm):
    class Meta:
        model = PositiveSmallIntegerField

class SlugFieldForm(FieldForm):
    class Meta:
        model = SlugField

class SmallIntegerFieldForm(FieldForm):
    class Meta:
        model = SmallIntegerField

class TimeFieldForm(FieldForm):
    class Meta:
        model = TimeField

class URLFieldForm(FieldForm):
    class Meta:
        model = URLField

class XMLFieldForm(FieldForm):
    class Meta:
        model = XMLField


