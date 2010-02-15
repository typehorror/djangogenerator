from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from project.models import Project
from application.models import Application
from models import Model

class ModelTest(TestCase):
    fixtures = ['user', 'project', 'application', 'model', 'form']
    username = 'username'
    password = 'password'
    email = 'username@example.com'
    project_name = 'test project'
    application_name = 'my_application'
    model_name = 'MyModel'

    def setUp(self):
        self.client = Client()

    def connect_user(self):
        """
        Connect the client using self.username and self password
        """
        self.client.login(username=self.username, password=self.password)

    def test_model_view(self):
        self.connect_user()
        model = Model.objects.get(name='TestModel')
        view_model_url = reverse('model_view', kwargs={'model_id':model.id})
        response = self.client.get(view_model_url)

        # check response
        self.failUnlessEqual(response.status_code, 200)
        
    def test_model_name_is_unique(self):
        """
        It is not possible to create two models with the same name 
        within the same application 
        """
        project = Project.objects.get(owner__username=self.username)
        application = project.applications.all()[0]
        model = application.models.all()[0]

        create_model_url = reverse('new_model_form', kwargs={'application_id': application.id})
        self.connect_user()

        # get the form prefix
        response = self.client.post(create_model_url)
        prefix = response.context['new_model_form'].prefix

        post_opts = {'%s-name' % prefix: model.name}
        response = self.client.post(create_model_url, post_opts)

        # check response
        self.failUnlessEqual(response.status_code, 200)

        # check that the objects has not been created
        self.assertEquals(Model.objects.filter(application=application).count(), 1L,
            'The view must not accept to create two models with the same name in the same application')

        # check the error presence
        self.assertFormError(response, 
                            'new_model_form',
                            'name',
                            '%s is already in use in this application' % model.name)

        

    def test_model_creation(self):
        self.connect_user()
        project = Project.objects.get(name=self.project_name)
        application = project.applications.all()[0]

        create_model_url = reverse('new_model_form', kwargs={'application_id': application.id})

        # get the form prefix
        response = self.client.post(create_model_url)
        prefix = response.context['new_model_form'].prefix
        post_opts = {'%s-name' % prefix: self.model_name}
        
        # create the model
        response = self.client.post(create_model_url, post_opts)

        # check response
        self.failUnlessEqual(response.status_code, 200)

        # check the model creation
        models = Model.objects.filter(name=self.model_name)
        self.assertEqual(models.count(), 1L,
            'The model has not been created by the view')

    def test_model_creation_same_name_different_application(self):
        """
        This test ensure to model with same name can be created if they
        are in a different application
        """
        self.connect_user()
        project = Project.objects.get(name=self.project_name)
        application = project.applications.all()[0]
        model = application.models.all()[0]

        create_application_url = reverse('new_application_form', kwargs={'project_id': project.id})

        # get the form prefix
        response = self.client.post(create_application_url)
        prefix = response.context['new_application_form'].prefix
        post_opts = {'%s-name' % prefix: self.application_name}
        
        # we create a new application
        response = self.client.post(create_application_url, post_opts)
        new_application = project.applications.get(name=self.application_name)
        
        # check response
        self.failUnlessEqual(response.status_code, 200)

        # we create a new model in this application using an existing model name
        create_model_url = reverse('new_model_form', kwargs={'application_id': new_application.id})

        # get the form prefix
        response = self.client.post(create_model_url)
        prefix = response.context['new_model_form'].prefix
        post_opts = {'%s-name' % prefix: model.name}
        
        response = self.client.post(create_model_url, post_opts)

        # check response
        self.failUnlessEqual(response.status_code, 200)
        
        # check that we have to models with this name in the same project
        models = Model.objects.filter(application__project=project, name=model.name)
        self.assertEqual(models.count(), 2L,
            'The model has not been created by the view')


    def test_model_name_casting_to_CamelCase(self):
        name_collection = { 'This is the name ': 'ThisIsTheName',
                            'ThisIsTheName2': 'ThisIsTheName2',
                            '   this   ': 'This',
                            '1 this is my name': 'ThisIsMyName'}
        self.connect_user()
        project = Project.objects.get(name=self.project_name)
        application = project.applications.all()[0]
        create_model_url = reverse('new_model_form', kwargs={'application_id': application.id})

        # get the form prefix
        response = self.client.post(create_model_url)
        prefix = response.context['new_model_form'].prefix

        for name, casted in name_collection.items():
            post_opts = {'%s-name' % prefix : name}
            response = self.client.post(create_model_url, post_opts)
            # check response
            self.failUnlessEqual(response.status_code, 200)
            self.assertTrue(casted == response.context['model'].name,
                'Error model name casting ("%s != %s")' % (casted, response.context['model'].name))
