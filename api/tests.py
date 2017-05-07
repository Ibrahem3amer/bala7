'''from django.test import TestCase
from rest_framework import status 
from rest_framework.test import APIClient
from django.core.urlresolvers import resolve


# Create your tests here.
class apiviewtest(TestCase):
	def setUp(self):
		self.client 			= APIClient()
		self.university_data 	= {'name':'test university', 'bio':'dadaadad', 'rank':'100'}
		self.response			= self.client.post(
				resolve('create_university'),
				self.university_data,
				format = 'json'
			)

	def test_api_save_post_request(self):
		# Setup test
		# Exercise test
		# Assert test
		self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)'''
