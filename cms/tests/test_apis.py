from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User
from cms.models import *
from users.models import Department, Faculty, University, UserProfile


class TopicAPITest(APITestCase):
    def test_return_list_of_topics(self):
        # Setup test
        url = reverse('api_topics_list')

        # Exercise test
        response = self.client.get(url)

        # Assert test
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MaterialAPITest(APITestCase):
    def setUp(self):
        self.uni        = University.objects.create(name = 'Test university')
        self.fac        = Faculty.objects.create(name = 'Test faculty')
        self.dep        = Department.objects.create(name = 'Test dep')
        self.topic      = Topic.objects.create(pk = 1, name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
        self.user       = User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f') 
        self.profile    = UserProfile.objects.create(user = self.user, department = self.dep, faculty = self.fac)

    def test_return_list_materials(self):
        # Setup test
        url = reverse('api_materials_list', kwargs={'topic_id': self.topic.id})
        
        # Exercise test
        self.user.profile.topics.add(self.topic)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        
        # Assert test
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_list_materials_with_unauthed_user(self):
        # Setup test
        url = reverse('api_materials_list', kwargs={'topic_id': self.topic.id})
        
        # Exercise test
        response = self.client.get(url)
        
        # Assert test
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_list_materials_with_unaccessed_topic(self):
        # Setup test
        url = reverse('api_materials_list', kwargs={'topic_id': self.topic.id})
        
        # Exercise test
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        
        # Assert test
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TaskAPITest(APITestCase):
    def setUp(self):
        self.uni        = University.objects.create(name = 'Test university')
        self.fac        = Faculty.objects.create(name = 'Test faculty')
        self.dep        = Department.objects.create(name = 'Test dep')
        self.topic      = Topic.objects.create(pk = 1, name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
        self.user       = User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f') 
        self.profile    = UserProfile.objects.create(user = self.user, department = self.dep, faculty = self.fac)

    def test_return_list_tasks_with_unauthed(self):
        # Setup test
        url = reverse('api_user_tasks')
        
        # Exercise test
        response = self.client.get(url)
        
        # Assert test
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)