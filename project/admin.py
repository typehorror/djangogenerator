from django.contrib import admin
from models import Project

class ProjectAdmin(admin.ModelAdmin):
    """
    Project admin page
    """
    search_fields = ('name', 'owner')
    list_filter = ('creation_date','modification_date')
    list_display = ('id', 'name', 'owner', 'creation_date','modification_date')


admin.site.register(Project, ProjectAdmin)
