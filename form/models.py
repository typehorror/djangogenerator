from django.db import models

class ModelForm(models.Model):
    model = models.ForeignKey("model.Model", related_name="model_forms")
    name = models.CharField(max_length=255)
    model_fields = models.ManyToManyField("field.ModelField")

    class Meta:
        unique_together = ("model", "name")
