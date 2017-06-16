from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User
from cms.models import *
from users.models import Department, Faculty


class TopicAPITest(APITestCase):
    def test_return_list_of_topics(self):
        # Setup test
        url = reverse('api_topics_list')

        # Exercise test
        response = self.client.get(url)

        # Assert test
        self.assertEqual(response.status_code, status.HTTP_200_OK)


