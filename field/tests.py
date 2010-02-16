from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from project.models import Project
from application.models import Application
from models import *
from model.models import Model

class FieldTest(TestCase):
    fixtures = ['user', 'project', 'application', 'model', 'form']
    username = 'username'
    password = 'password'
    email = 'username@example.com'
    project_name = 'test project'
    application_name = 'my_application'
    model_name = 'MyModel'
    field_name = 'test_field'

    def setUp(self):
        self.client = Client()

    def insert_field(self, model, name='test_field', field_type='CharField', **options):
        """
        insert a new CharField in the model using a url view call
        return a model_field containing the field as model_field.object
        options are passed to the creation view and used to generate the field.
        """
        options.update({'name':name})
        new_model_field_url = reverse('new_model_field_form', kwargs={'field_type': field_type, 'model_id':model.id})

        # get the form prefix
        response = self.client.post(new_model_field_url)
        prefix = response.context['new_field_form'].prefix
        
        # Add the prefix to the options passed to the form
        options = dict([ ('%s-%s' % (prefix,name), value) for name, value in options.items() ])

        # create the field
        response = self.client.post(new_model_field_url, options)

        # get the last created model field
        return response

    def connect_user(self):
        """
        Connect the client using self.username and self password
        """
        self.client.login(username=self.username, password=self.password)

    def test_field_view(self):
        self.connect_user()

        # lets insert a field into the project
        response = self.insert_field(Model.objects.all()[0], max_length=255)
        model_field = response.context['model_field']
        field = model_field.object

        view_field_url = reverse('model_field_form', kwargs={'model_field_id':model_field.id,
                                                       'field_type': field.field_type})
        response = self.client.get(view_field_url)

        # check response
        self.failUnlessEqual(response.status_code, 200)
        
    def test_field_name_is_unique(self):
        """
        It is not possible to create two fields with the same name 
        within the same model 
        """
        field_name = 'my_test_field'
        field_type_1 = 'CharField'
        field_type_2 = 'IntegerField'
        model = Model.objects.all()[0]
        
        self.connect_user()
        
        # the first field creation must succeed
        response = self.insert_field(model, max_length=255, field_type='CharField', name=field_name)
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(CharField.objects.filter(name=field_name).count(), 1L)

        # the second field creation must fail
        response = self.insert_field(model, max_length=255, field_type='CharField', name=field_name)
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(CharField.objects.filter(name=field_name).count(), 1L)

        # ... even if it is another field type
        response = self.insert_field(model, default=0, field_type='IntegerField', name=field_name)
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(IntegerField.objects.filter(name=field_name).count(), 0L)

    def test_field_creation_same_name_different_model(self):
        """
        This test ensure that 2 fields with same name can be created if they
        are in a different model.
        """
        field_name = 'my_test_field'
        field_type ='CharField'

        self.connect_user()
        model = Model.objects.all()[0]

        create_model_url = reverse('new_model_form', kwargs={'application_id': model.application.id})

        # get the form prefix
        response = self.client.post(create_model_url)
        prefix = response.context['new_model_form'].prefix
        post_opts = {'%s-name' % prefix: self.model_name}
        
        # we create a new model
        response = self.client.post(create_model_url, post_opts)
        self.failUnlessEqual(response.status_code, 200)
        new_model = response.context['model']

        # no charfield must exist before creation
        self.assertEqual(CharField.objects.filter(name=field_name).count(), 0L)
        
        # we create a new field in a model
        respones = self.insert_field(model, max_length=255, field_type=field_type, name=field_name)
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(CharField.objects.filter(name=field_name).count(), 1L)

        # we create a new field in another model using the same field name
        response = self.insert_field(new_model, max_length=255, field_type=field_type, name=field_name)
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(CharField.objects.filter(name=field_name).count(), 2L)
        
    def test_field_name_casting(self):
        name_collection = { 'This is the name ': 'this_is_the_name',
                            'ThisIsTheName2': 'thisisthename2',
                            '   this   ': 'this',
                            '1 this is my name': 'this_is_my_name'}
        self.connect_user()
        model = Model.objects.all()[0]

        for name, casted in name_collection.items():
            response = self.insert_field(model, max_length=255, field_type='CharField', name=name)
            # check response
            self.failUnlessEqual(response.status_code, 200)
            self.assertTrue(casted == response.context['model_field'].object.name,
                'Error field name casting ("%s != %s")' % (casted, response.context['model_field'].object.name))
