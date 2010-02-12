from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from project.models import Project
from application.models import Application

class ProjectTest(TestCase):
    fixtures = ['user', 'project', 'application', 'model', 'form']
    username = 'username'
    password = 'password'
    email = 'username@example.com'
    project_name = 'test project'
    application_name = 'my_application'

    def setUp(self):
        self.client = Client()

    def connect_user(self):
        """
        Connect the client using self.username and self password
        """
        self.client.login(username=self.username, password=self.password)

    def test_application_name_is_unique(self):
        """
        It is not possible to create two application with the same name
        withing the same project
        """
        project = Project.objects.get(owner__username=self.username)
        application = project.applications.all()[0]

        create_project_url = reverse('new_application_form', kwargs={'project_id': project.id})
        self.connect_user()
        response = self.client.post(create_project_url, {'new_application_-name':application.name})

        # check response
        self.failUnlessEqual(response.status_code, 200)

        # check the error presence

        self.assertEquals(Application.objects.filter(project=project).count(), 1L,
            'The view must not accept to create two applicationis with the same name in the same project')

        self.assertFormError(response, 
                            'new_application_form',
                            'name',
                            '%s is already in use in this project' % application.name)

        

    def test_application_creation(self):
        self.connect_user()
        project = Project.objects.get(name=self.project_name)
        create_project_url = reverse('new_application_form', kwargs={'project_id': project.id})
        response = self.client.post(create_project_url, {'new_application_-name':self.application_name})

        # check response
        self.failUnlessEqual(response.status_code, 200)

        # check the creation
        applications = Application.objects.filter(name=self.application_name)
        self.assertEqual(applications.count(), 1L,
            'The application has not been created by the view')

    def test_application_name_casting(self):
        name_collection = { 'This is the name ': 'this_is_the_name',
                            '     h   ': 'h',
                            '~!@#$^&*()ff': 'ff'}
        self.connect_user()
        project = Project.objects.get(name=self.project_name)
        create_application_url = reverse('new_application_form', kwargs={'project_id': project.id})
        for name, casted in name_collection.items():
            response = self.client.post(create_application_url, {'new_application_-name': name})
            # check response
            self.failUnlessEqual(response.status_code, 200)
            self.assertTrue(Application.objects.filter(name=casted).count() == 1,
                'Error application name casting ("%s")' % name)
