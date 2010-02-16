from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from project.models import Project
from application.models import Application

class ApplicationTest(TestCase):
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

        create_application_url = reverse('new_application_form', kwargs={'project_id': project.id})
        self.connect_user()
        # get the prefix
        response = self.client.post(create_application_url)
        prefix = response.context['new_application_form'].prefix
        post_opts = {'%s-name' % prefix : application.name}

        response = self.client.post(create_application_url, post_opts)

        # check response
        self.failUnlessEqual(response.status_code, 200)

        # check the error presence
        self.assertEquals(Application.objects.filter(project=project).count(), 1L,
            'The view must not accept to create two applicationis with the same name in the same project')

        self.assertFormError(response, 
                            'new_application_form',
                            'name',
                            '%s is already in use in this project' % application.name)

    def test_application_view(self):
        self.connect_user()
        application = Application.objects.get(name='test_application')
        view_application_url = reverse('application_view', kwargs={'application_id': application.id})
        response = self.client.get(view_application_url)

        # check response
        self.failUnlessEqual(response.status_code, 200)
        

    def test_application_creation(self):
        self.connect_user()
        project = Project.objects.get(name=self.project_name)
        create_application_url = reverse('new_application_form', kwargs={'project_id': project.id})

        # get the prefix
        response = self.client.post(create_application_url)
        prefix = response.context['new_application_form'].prefix
        post_opts = {'%s-name' % prefix : self.application_name}

        response = self.client.post(create_application_url, post_opts)

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
        # get the prefix
        response = self.client.post(create_application_url)
        prefix = response.context['new_application_form'].prefix

        for name, casted in name_collection.items():
            post_opts = {'%s-name' % prefix : name}
            response = self.client.post(create_application_url, post_opts)
            # check response
            self.failUnlessEqual(response.status_code, 200)
            application = response.context['application']
            self.assertTrue(application.name == casted,
                'Error application name casting ("%s!=%s")' % (casted, application.name))
