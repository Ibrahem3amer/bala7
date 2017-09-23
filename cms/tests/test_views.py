from django.core.urlresolvers import resolve
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.http import HttpRequest, Http404
from django.contrib.auth.models import User
from unittest import skip
from users.models import University, Faculty, Department, UserProfile
from cms.models import Topic
from cms.views import get_topic 


class AccessRestriction(TestCase):
    def setUp(self):
        self.user           = User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
        self.uni            = University.objects.create(name = 'test_university')
        self.fac            = Faculty.objects.create(name = 'Test faculty')
        self.dep            = Department.objects.create(name = 'Test dep')
        self.profile        = UserProfile.objects.create(university = self.uni, faculty = self.fac, department = self.dep)
        self.topic          = Topic.objects.create(name = 'cs', desc = "test test test", faculty = self.fac, term = 1)
        self.topic.department.add(self.dep)
        self.user.profile   = self.profile
        self.profile.topics.add(self.topic)
    
    def test_return_topic_that_match_user(self):
        # Setup test
        request         = RequestFactory()
        request         = request.get(reverse('get_topic', kwargs={'dep_id': self.dep.id, 'topic_id': self.topic.id}))
        request.user    = self.user

        # Exercise test
        response = get_topic(request, self.dep.id, self.topic.id)
        
        # Assert test
        self.assertEqual(200, response.status_code)

    def test_return_topic_that_has_different_department(self):
        # Setup test
        request         = RequestFactory()
        request         = request.get(reverse('get_topic', kwargs={'dep_id': self.dep.id, 'topic_id': self.topic.id}))
        request.user    = self.user

        # Exercise test
        another_dep = Department.objects.create() 
        try:
            response    = get_topic(request, another_dep.id, self.topic.id)
            flag        = False
        except Http404:
            flag        = True
        

        # Assert test
        self.assertTrue(flag)

    def test_return_topic_that_does_not_exist(self):
        # Setup test
        request         = RequestFactory()
        request         = request.get(reverse('get_topic', kwargs={'dep_id': self.dep.id, 'topic_id': self.topic.id}))
        request.user    = self.user

        # Exercise test
        try:
            response    = get_topic(request, self.dep.id, 990)
            flag        = False
        except Http404:
            flag        = True
        

        # Assert test
        self.assertTrue(flag)

    def test_return_topic_that_outside_user_topics(self):
        # Setup test
        another_topic   = Topic.objects.create(name = 'is', desc = "test test test", faculty = self.fac, term = 1)
        another_topic.department.add(self.dep)
        self.user.profile.topics.add(another_topic)        
        request         = RequestFactory()
        request         = request.get(reverse('get_topic', kwargs={'dep_id': self.dep.id, 'topic_id': self.topic.id}))
        request.user    = self.user

        # Exercise test
        outsider_topic  = Topic.objects.create(name = 'ms', desc = "test test test", faculty = self.fac, term = 1)
        outsider_topic.department.add(self.dep)
        try:
            response    = get_topic(request, self.dep.id, outsider_topic.id)
            flag        = False
        except Http404:
            flag        = True

        # Assert test
        self.assertTrue(flag)


    def test_get_topic_with_no_parameters(self):
        # Setup test
        another_topic   = Topic.objects.create(name = 'is', desc = "test test test", faculty = self.fac, term = 1)
        another_topic.department.add(self.dep)
        self.user.profile.topics.add(another_topic)        
        request         = RequestFactory()
        request         = request.get(reverse('get_topic', kwargs={'dep_id': self.dep.id, 'topic_id': self.topic.id}))
        request.user    = self.user

        # Exercise test
        outsider_topic  = Topic.objects.create(name = 'ms', desc = "test test test", faculty = self.fac, term = 1)
        outsider_topic.department.add(self.dep)
        try:
            response    = get_topic(request)
            flag        = False
        except Http404:
            flag        = True

        # Assert test
        self.assertTrue(flag)

class TableViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ssss', email='tesssst@test.com', password='secrettt23455')
        self.fac = Faculty.objects.create()
        self.dep = Department.objects.create(faculty=self.fac)
        self.profile = UserProfile.objects.create(user=self.user, department=self.dep, faculty=self.fac)
        
    def test_page_load_on_get(self):
        # Setup test
        url = reverse('web_dep_table')
        request = self.client.login(username="ssss", password="secrettt23455")

        # Exercise test
        request = self.client.get(url)

        # Assert test
        self.assertEqual(200, request.status_code)
        self.assertTemplateUsed(request, 'tables/table_main.html')

    def test_page_redirect_on_post(self):
        # Setup test
        url = reverse('web_dep_table')
        request = self.client.login(username="ssss", password="secrettt23455")

        # Exercise test
        request = self.client.post(url)

        # Assert test
        self.assertEqual(302, request.status_code)

    def test_page_redirect_on_no_profile(self):
        # Setup test
        user = User.objects.create_user(
            username='test_username',
            email='tesssst@test.com',
            password='secrettt23455'
        )
        url = reverse('web_dep_table')
        request = self.client.login(username="test_username", password="secrettt23455")

        # Exercise test
        request = self.client.get(url)

        # Assert test
        self.assertEqual(302, request.status_code)

class UserTableViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'ssss', email = 'tesssst@test.com', password = 'secrettt23455')
        self.fac = Faculty.objects.create()
        self.dep = Department.objects.create(faculty = self.fac)
        UserProfile.objects.create(user=self.user, department = self.dep, faculty = self.fac)
        self.topic = Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1)
        self.topic.department.add(self.dep)

    def test_page_load_on_get(self):
        # Setup test
        url = reverse('web_user_table')
        request = self.client.login(username="ssss", password="secrettt23455")

        # Exercise test
        request = self.client.get(url)

        # Assert test
        self.assertEqual(200, request.status_code)
        self.assertTemplateUsed(request, 'tables/user_table.html')

    def test_page_load_if_no_profile(self):
        # Setup test
        url = reverse('web_user_table')
        another_user = User.objects.create_user(username = 'xxxss', email = 'tesssst@test.com', password = 'secrettt23455')
        request = self.client.login(username="xxxss", password="secrettt23455")

        # Exercise test
        request = self.client.get(url)

        # Assert test
        self.assertEqual(200, request.status_code)
        self.assertTemplateUsed(request, 'tables/user_table.html')

    def test_post_when_no_choices(self):
        # Setup test
        url = reverse('web_user_table')
        data = {}
        request = self.client.login(username="xxxss", password="secrettt23455")

        # Exercise test
        request = self.client.post(url, data=data)

        # Assert test
        self.assertEqual(302, request.status_code)