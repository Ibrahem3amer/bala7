from django.core.urlresolvers import resolve
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.http import HttpRequest, Http404
from django.contrib.auth.models import User
from unittest import skip
from users.models import University, Faculty, Department, UserProfile
from cms.models import Topic
from cms.views import get_topic 


class Access_restriction(TestCase):
    def setUp(self):
        self.user           = User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
        self.uni            = University.objects.create(name = 'test_university')
        self.fac            = Faculty.objects.create(name = 'Test faculty')
        self.dep            = Department.objects.create(name = 'Test dep')
        self.profile        = UserProfile.objects.create(university = self.uni, faculty = self.fac, department = self.dep)
        self.topic          = Topic.objects.create(name = 'cs', desc = "test test test", department = self.dep, faculty = self.fac, term = 1)
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
        another_topic   = Topic.objects.create(name = 'is', desc = "test test test", department = self.dep, faculty = self.fac, term = 1)
        self.user.profile.topics.add(another_topic)        
        request         = RequestFactory()
        request         = request.get(reverse('get_topic', kwargs={'dep_id': self.dep.id, 'topic_id': self.topic.id}))
        request.user    = self.user

        # Exercise test
        outsider_topic  = Topic.objects.create(name = 'ms', desc = "test test test", department = self.dep, faculty = self.fac, term = 1)
        try:
            response    = get_topic(request, self.dep.id, outsider_topic.id)
            flag        = False
        except Http404:
            flag        = True

        # Assert test
        self.assertTrue(flag)


    def test_get_topic_with_no_parameters(self):
        # Setup test
        another_topic   = Topic.objects.create(name = 'is', desc = "test test test", department = self.dep, faculty = self.fac, term = 1)
        self.user.profile.topics.add(another_topic)        
        request         = RequestFactory()
        request         = request.get(reverse('get_topic', kwargs={'dep_id': self.dep.id, 'topic_id': self.topic.id}))
        request.user    = self.user

        # Exercise test
        outsider_topic  = Topic.objects.create(name = 'ms', desc = "test test test", department = self.dep, faculty = self.fac, term = 1)
        try:
            response    = get_topic(request)
            flag        = False
        except Http404:
            flag        = True

        # Assert test
        self.assertTrue(flag)