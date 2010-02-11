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

    def test_project_del(self):
        self.connect_user()

        # make sure the user just have 1 project
        projects = Project.objects.filter()
        self.assertTrue(projects.count() == 1L, 
            'user "username" must have only one project in fixture project.json')

        project = projects[0]
        application_ids = project.applications.values_list('id', flat=True)
        model_ids = Model.objects.filter(application__project = project).values_list('id', flat=True)
        form_ids = ModelForm.objects.filter(model__application__project = project).values_list('id', flat=True)

        # lets insert a field into the project
        model = Model.objects.filter(application__project=project)[0]
        new_model_field_url = reverse('new_model_field_form', kwargs={'field_type':'CharField', 'model_id':model.id})
        prefix = 'CharField_%d-' % model.id
        response = self.client.post(new_model_field_url, {'%sname' % prefix :'test_field', '%smax_length' % prefix :255})
        self.assertEqual(response.status_code, 200,
            'The field creation using the view call (%s) did not behavior has expected (verify the prefix).' % new_model_field_url)
        model_field = model.model_fields.all()[0]
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


