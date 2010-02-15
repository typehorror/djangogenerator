# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from models import Project
from application.models import Application
from model.models import Model
from form.models import ModelForm
from field.models import ModelField, CharField

class ProjectTest(TestCase):
    fixtures = ['user', 'project', 'application', 'model', 'form']
    username = 'username'
    password = 'password'
    email = 'username@example.com'
    project_name = 'my project'

    def setUp(self):
        self.client = Client()

    def connect_user(self):
        self.client.login(username=self.username, password=self.password)
    
    def test_project_detail_view(self):
        project = Project.objects.get(name='test project')
        view_project_detail_url = reverse('project_view', kwargs={'project_id': project.id})

        self.connect_user()
        response = self.client.get(view_project_detail_url)

        # Check response
        self.assertEqual(response.status_code, 200)
        

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

    def test_project_generate(self):
        self.connect_user()
        # make sure the user just have 1 project
        projects = Project.objects.filter(owner__username=self.username)
        project = projects[0]

        generate_project_url = reverse('project_generate', kwargs={'project_id':project.id})
        response = self.client.post(generate_project_url)

        models = Model.objects.filter(application__project=project)
        model = models[0]
        self.insert_field(model, max_length=255, help_text = u'\xf6 in unicode')
        model.save()

        # ensure it's working using a field with an unicode name
        generate_project_url = reverse('project_generate', kwargs={'project_id':project.id})
        response = self.client.post(generate_project_url)

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
        self.assertTrue(response.context.has_key('model_field'),
            'Field creation failed with options %s' % options)

        # get the last created model field
        return response.context['model_field']

    def test_project_del(self):
        self.connect_user()

        # make sure the user just have 1 project
        projects = Project.objects.filter(owner__username=self.username)
        self.assertTrue(projects.count() == 1L, 
            'user "username" must have only one project in fixture project.json')

        project = projects[0]
        application_ids = project.applications.values_list('id', flat=True)
        model_ids = Model.objects.filter(application__project = project).values_list('id', flat=True)
        form_ids = ModelForm.objects.filter(model__application__project = project).values_list('id', flat=True)

        # lets insert a field into the project
        model_field = self.insert_field(Model.objects.filter(application__project=project)[0], max_length=255)
        field = model_field.object

        # call delete function
        delete_project_url = reverse('project_del', kwargs={'project_id': project.id})
        response = self.client.post(delete_project_url)
        self.assertEqual(response.status_code, 200,
            'The call the del view (%s) does not behavior has expected.' % delete_project_url)

        # test project doesn't exist anymore
        projects = Project.objects.filter()
        self.assertTrue(projects.count() == 0,
            'project has not been deleted by the del view call')

        # test contained Application doesn't exist anymore
        applications = Application.objects.filter(pk=application_ids)
        self.assertTrue(applications.count() == 0,
            'applications linked to the project has not been deleted')

        # test contained Model doesn't exist anymore
        models = Model.objects.filter(pk=model_ids)
        self.assertTrue(models.count() == 0,
            'models linked to application has not been deleted')

        # test contained form doesn't exist anymore
        forms = ModelForm.objects.filter(pk=form_ids)
        self.assertTrue(forms.count() == 0,
            'form linked to the model has not been deleted')

        # test contained ModelField doesn't exist anymore
        self.assertTrue(ModelField.objects.filter(pk=model_field.id).count() == 0,
            'model_field linked to model has not been deleted')

        # test contained field doesn't exist anymore
        self.assertTrue(CharField.objects.filter(pk=field.id).count() == 0,
            'field linked to model_field has not been deleted')


