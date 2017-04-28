from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from users.views import home_visitor, display_signup
from users.models import University

class user_vists_homepage(TestCase):
	def test_user_find_homepage(self):
		# Setup test
		request = resolve('/')

		# Exercise test

		# Assert test
		self.assertEqual(request.func, home_visitor)

	def test_home_visitor_returns_correct_html(self):
		# Setup test
		request = HttpRequest()

		# Exercise test
		response = self.client.get('/')
		expected_html = response.content.decode('utf-8')

		# Assert test
		self.assertTemplateUsed(response, 'home_visitor.html')

	def test_user_finds_signup(self):
		# Setup test
		request = resolve('/users/signup/')

		# Exercise test
		# Assert test
		self.assertEqual(request.func, display_signup)

	def test_signup_returns_correct_output(self):
		# Setup test
		response = self.client.get('/users/signup')

		# Exercise test
		# Assert test
		self.assertTemplateUsed(response, 'signup.html')

class UniversityModelTest(TestCase):
	
	def test_save_university(self):
		# Setup test
		mansoura_university = University()
		mansoura_university.uni_type = 'public'
		mansoura_university.save()
		kfs_university = University()
		kfs_university.uni_type = 'private'
		kfs_university.save()

		# Exercise test
		saved_universities = University.objects.all()

		# Assert test
		self.assertEqual(saved_universities.count(), 2)

	def test_retreive_university(self):
		# Setup test
		mansoura_university = University()
		mansoura_university.bio = 'a public university'
		mansoura_university.save()

		# Exercise test
		saved_university = University.objects.first()

		# Assert test
		self.assertEqual('a public university', saved_university.bio)
		