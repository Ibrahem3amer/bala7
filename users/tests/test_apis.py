from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from users.models import University, Faculty, Department

class UsersAPITest(APITestCase):
	def test_return_list_of_users(self):
		# Setup test
		url = reverse('api_users_list')

		# Exercise test
		response = self.client.get(url)

		# Assert test
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_add_new_user(self):
		# Setup test
		url 	= reverse('api_users_list')
		data 	= {'username':'waelll', 'email':'teststest@hhhh.com', 'password':'22222222255555hhem', 'password_confirmation':'22222222255555hhem'}
		
		# Exercise test
		response = self.client.post(url, data)

		# Assert test
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(User.objects.get().username, 'waelll')

	def test_add_new_user_with_invalid_username(self):
		# Setup test
		url 	= reverse('api_users_list')
		data 	= {'username':'123wael', 'email':'teststest@hhhh.com', 'password':'22222222255555hhem', 'password_confirmation':'22222222255555hhem'}
		
		# Exercise test
		response = self.client.post(url, data)

		# Assert test
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(User.objects.count(), 0)

	def test_add_new_user_with_invalid_email(self):
		# Setup test
		url 	= reverse('api_users_list')
		data 	= {'username':'wwwweee', 'email':'teststest@hcom', 'password':'22222222255555hhem', 'password_confirmation':'22222222255555hhem'}
		
		# Exercise test
		response = self.client.post(url, data)

		# Assert test
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(User.objects.count(), 0)

	def test_get_specific_user(self):
		# Setup test
		url = reverse('api_user', kwargs={'pk':1})
		u = User.objects.create(username = 'ididididid', email = 'sdsadasd@test.com', password = '111115555888dddd')

		# Exercise test
		response = self.client.get(url)

		# Assert test
		self.assertEqual(response.data, {'id':1, 'username':'ididididid', 'email': 'sdsadasd@test.com', 'password': '111115555888dddd'})

	def test_get_list_of_univs(self):
		# Setup test
		url = reverse('api_univs_list')

		# Exercise test
		response = self.client.get(url)

		# Assert test
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_univ_linked(self):
		# Setup test
		University.objects.create()
		url = reverse('api_univ', kwargs={'pk':1})

		# Exercise test
		response = self.client.get(url)

		# Assert test
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		