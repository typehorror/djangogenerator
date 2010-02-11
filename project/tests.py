from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from models import Project

class ProjectTest(TestCase):
    fixtures = ['user', 'project']
    username = 'username'
    password = 'password'
    email = 'username@example.com'
    project_name = 'project_name'
    application_name = 'application_name'
    model_name = 'model_name'
    field_type = 'CharField'
    field_name = 'myCharField'

    def setUp(self):
        self.client = Client()

    def connect_user(self):
        self.client.login(username=self.username, password=self.password)

    def test_project_list_view(self):
        from forms import NewProjectForm
        view_project_list_url = reverse('project_list')

        self.connect_user()
        response = self.client.get(view_project_list_url)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        # Check response contains a form
        self.assertEqual(response.context['new_project_form'].as_p(), NewProjectForm().as_p()) 

    def test_project_creation(self):
        self.connect_user()
        create_project_url = reverse('project_list')
        response = self.client.post(create_project_url, {'name':self.project_name})
        # check that the response
        self.assertEqual(response.status_code, 200)

        projects = Project.objects.filter(name=self.project_name)
        # check the creation
        self.assertEqual(projects.count(), 1L)
        
        # check that the object is contain in the response
        self.assertTrue(projects[0] in response.context['projects'].object_list)
