import json
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
        self.uni = University.objects.create(name = 'Test university')
        self.fac = Faculty.objects.create(name = 'Test faculty')
        self.dep = Department.objects.create(name = 'Test dep')
        self.topic = Topic.objects.create(pk = 1, name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
        self.user = User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f') 
        self.profile = UserProfile.objects.create(user = self.user, department = self.dep, faculty = self.fac)

    def test_return_list_tasks_with_unauthed(self):
        # Setup test
        url = reverse('api_user_tasks')
        
        # Exercise test
        response = self.client.get(url)
        
        # Assert test
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class QueryTableAPITest(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name = 'Test university')
        self.fac = Faculty.objects.create(name = 'Test faculty')
        self.dep = Department.objects.create(name = 'Test dep')
        self.topic = Topic.objects.create(pk = 1, name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
        self.topic2 = Topic.objects.create(pk = 2, name = 'test topic2 with spaces', desc = 'ddddd', term = 2, department = self.dep, weeks = 5)
        self.user = User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f') 
        self.profile = UserProfile.objects.create(user = self.user, department = self.dep, faculty = self.fac)
        self.profile.topics.add(self.topic)
        self.profile.topics.add(self.topic2)

    def test_auth_user_query_table_with_topics(self):
        # Setup test
        topics = [['']*6 for i in range(7)]
        places = [['']*6 for i in range(7)]
        topics[1][1] = 'Lecture'
        places[1][1] = 'Hall 1'
        topics[1][3] = 'Section'
        places[1][3] = 'Hall 2'
        TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
        topics[4][4] = 'another_lecture'
        places[4][4] = 'another_lecture'
        TopicTable.objects.create(topic=self.topic2, topics=topics, places=places)
        topics_list = [self.topic.id, self.topic2.id]
        data = {'topics': topics_list}
        
        # Exercise test
        url = reverse('api_query_table')
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.post(url, data=data)

        # Assert test
        self.assertNotEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        list_response = json.loads(request.data)
        self.maxDiff = None
        self.assertIn(topics[1][1]+'\n'+places[1][1], list_response[1][1])
        self.assertIn(topics[1][3]+'\n'+places[1][3], list_response[1][3])
        self.assertIn(topics[4][4]+'\n'+places[4][4], list_response[4][4])

    def test_auth_user_query_table_with_days(self):
        # Setup test
        topics = [['']*6 for i in range(7)]
        places = [['']*6 for i in range(7)]
        topics[1][1] = 'Lecture'
        places[1][1] = 'Hall 1'
        topics[1][3] = 'Section'
        places[1][3] = 'Hall 2'
        TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
        topics[4][4] = 'another_lecture'
        places[4][4] = 'another_lecture'
        TopicTable.objects.create(topic=self.topic2, topics=topics, places=places)
        data = {'days': 1}
        
        # Exercise test
        url = reverse('api_query_table')
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.post(url, data=data)

        # Assert test
        self.assertNotEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        list_response = json.loads(request.data)
        self.assertIn(topics[1][1]+'\n'+places[1][1], list_response[1][1])
        self.assertIn(topics[1][3]+'\n'+places[1][3], list_response[1][3])
        self.assertNotIn(topics[4][4]+'\n'+places[4][4], list_response[4][4])

    def test_unauth_user_query_table(self):
        # Setup test
        data = {'days': 1}
        
        # Exercise test
        url = reverse('api_query_table')
        request = self.client.post(url, data=data)

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_with_no_profile_query_table(self):
        # Setup test
        user2 = User.objects.create_user(username = 'sssss', email = 'test_@test.com', password = '000000555555ddd5f5f') 
        data = {'days': 1}
        
        # Exercise test
        url = reverse('api_query_table')
        request = self.client.login(username="sssss", password="000000555555ddd5f5f")
        request = self.client.post(url, data=data)

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertNotIn('\n', request.data)

class MainTableAPITest(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name = 'Test university')
        self.fac = Faculty.objects.create(name = 'Test faculty')
        self.dep = Department.objects.create(name = 'Test dep')
        self.topic = Topic.objects.create(pk = 1, name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
        self.topic2 = Topic.objects.create(pk = 2, name = 'test topic2 with spaces', desc = 'ddddd', term = 2, department = self.dep, weeks = 5)
        self.user = User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f') 
        self.profile = UserProfile.objects.create(user = self.user, department = self.dep, faculty = self.fac)
        self.profile.topics.add(self.topic)
        self.profile.topics.add(self.topic2)

    def test_auth_user_displays_main_table(self):
        # Setup test
        topics = [['']*6 for i in range(7)]
        places = [['']*6 for i in range(7)]
        topics[1][1] = 'Lecture'
        places[1][1] = 'Hall 1'
        topics[1][3] = 'Section'
        places[1][3] = 'Hall 2'
        TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
        topics[4][4] = 'another_lecture'
        places[4][4] = 'another_lecture'
        TopicTable.objects.create(topic=self.topic2, topics=topics, places=places)

        # Exercise test
        url = reverse('api_main_table', kwargs={'user_id': self.user.id})
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.get(url)

        # Assert test
        self.assertNotEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        list_response = json.loads(request.data)
        self.maxDiff = None
        self.assertIn(topics[1][1]+'\n'+places[1][1], list_response[0][1][1])
        self.assertIn(topics[1][3]+'\n'+places[1][3], list_response[0][1][3])
        self.assertIn(topics[4][4]+'\n'+places[4][4], list_response[1][4][4])

    def test_user_with_no_profile_displays_main_table(self):
        # Setup test
        user2 = User.objects.create_user(username = 'sssss', email = 'test_@test.com', password = '000000555555ddd5f5f') 
        data = {'days': 1}
        
        # Exercise test
        url = reverse('api_main_table', kwargs={'user_id': user2.id})
        request = self.client.login(username="sssss", password="000000555555ddd5f5f")
        request = self.client.get(url, data=data)

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)