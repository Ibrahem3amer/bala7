from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.core.exceptions import ValidationError 
from unittest import skip
from django.contrib.auth.models import User
from cms.models import Topic, Material
from cms.forms import AddMaterialForm
from users.models import University, Faculty, Department, UserProfile

class AddMaterialFormTest(TestCase):
    def setUp(self):
        self.uni            = University.objects.create(name = 'Test university')
        self.fac            = Faculty.objects.create(name = 'Test faculty')
        self.dep            = Department.objects.create(name = 'Test dep')
        self.topic          = Topic.objects.create(pk = 1, name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
        self.user           = User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f')
        self.profile        = UserProfile.objects.create(user = self.user, department = self.dep, faculty = self.fac)
        self.material       = Material.objects.create(
                name            = 'test_material',
                content         = 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
                link            = 'http://onedrive.live.com/',
                year            = '2017-1-5',
                term            = 1,
                content_type    = 1,
                week_number     = 1,
                user            = self.user,
                topic           = self.topic
            )
        

    def test_intiaite_basic_form(self):
        # Setup test
        data = {
            'user': 1,
            'topic': 1,
            'name': 'material',
            'content': 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
            'link': 'http://files2.syncfusion.com/Downloads/Ebooks/HTTP_Succinctly.pdf',
            'year': '2015-1-5',
            'term': 1,
            'content_type': 1,
            'week_number': 0,
        }

        # Exercise test
        form = AddMaterialForm(data = data)
        
        # Assert test
        self.assertTrue(form.is_valid())


    def test_add_material_with_year_in_future(self):
        # Setup test
        data = {
            'user': 1,
            'topic': 1,
            'name': 'material',
            'content': 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
            'link': 'https://docs.google.com',
            'year': '2123-1-5',
            'term': 1,
            'content_type': 1,
            'week_number': 0,
        }


        # Exercise test
        form = AddMaterialForm(data = data)
        
        # Assert test
        self.assertFalse(form.is_valid())

    def test_add_material_with_repeated_link(self):
        # Setup test
        data = {
            'user': 1,
            'topic': 1,
            'name': 'material',
            'content': 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
            'link': 'http://onedrive.live.com/',
            'year': '2017-1-5',
            'term': 1,
            'content_type': 1,
            'week_number': 0,
        }

        # Exercise test
        form = AddMaterialForm(data = data)
        
        # Assert test
        self.assertFalse(form.is_valid())      
