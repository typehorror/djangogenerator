from django.db import models

# Create your models here.
class Application(models.Model):
    project = models.ForeignKey('project.Project', related_name='applications')
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return self.name

