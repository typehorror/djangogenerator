from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
    url(r'public/list/$', 'public_project_list', name='public_project_list'),
    url(r'public/view/(?P<project_id>\d+)/$', 'public_project_view', name='public_project_view'),
    url(r'public/generate/(?P<project_id>\d+)/$', 'public_project_generate', name='public_project_generate'),
    url(r'del/(?P<project_id>\d+)/$', 'project_del', name='project_del'),
    url(r'list/$', 'project_list', name='project_list'),
    url(r'view/(?P<project_id>\d+)/$', 'project_view', name='project_view'),
    url(r'generate/(?P<project_id>\d+)/$', 'project_generate', name='project_generate'),
    )
 
