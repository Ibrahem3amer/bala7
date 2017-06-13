from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cms.models import *
from users.models import Department


class TopicAPITest(APITestCase):
    def test_return_list_of_topics(self):
        # Setup test
        url = reverse('api_topics_list')

        # Exercise test
        response = self.client.get(url)

        # Assert test
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_topic_with_correct_id(self):
        # Setup test
        dep         = Department.objects.create()
        new_topic   = Topic.objects.create(name = 'topic_new_2', desc = 'ddddd', term = 1, department = dep)
        url         = reverse('api_topic', kwargs={'pk':new_topic.id})

        # Exercise test
        response = self.client.get(url)
        
        # Assert test
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_topic.name)

    def test_return_topic_with_incorrect_id(self):
        # Setup test
        dep         = Department.objects.create()
        new_topic   = Topic.objects.create(name = 'topic_new_2', desc = 'ddddd', term = 1, department = dep)
        url         = reverse('api_topic', kwargs={'pk':new_topic.id+1})

        # Exercise test
        response = self.client.get(url)
        
        # Assert test
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


