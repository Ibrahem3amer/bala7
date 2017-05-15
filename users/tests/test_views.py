from django.core.urlresolvers import resolve
from django.urls import reverse
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from unittest import skip
from users.views import home_visitor, display_signup
from users.models import University, Faculty, Department
from users.forms import SignupForm, UserSignUpForm

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
		request = resolve(reverse('web_signup'))

		# Exercise test
		# Assert test
		self.assertEqual(request.func, display_signup)

	def test_signup_returns_correct_output(self):
		# Setup test
		response = self.client.get(reverse('web_signup'))

		# Exercise test
		# Assert test
		self.assertEqual(200, response.status_code)
		self.assertTemplateUsed(response, 'signup.html')
	
	def test_second_form_get_with_data(self):
		# Setup test
		response = self.client.get(reverse('web_signup_second_form'), data={'selected_university':1, 'selected_faculty':1, 'selected_department':1})
		# Exercise test
		# Assert test
		self.assertEqual(200, response.status_code)

	def test_second_form_get_with_no_data(self):
		# Setup test
		response = self.client.get(reverse('web_signup_second_form'), data={})
		# Exercise test
		# Assert test
		self.assertEqual(302, response.status_code)


	def test_second_form_post_with_data(self):
		# Setup test
		first_form_data 			= {'university':1, 'faculty':1, 'department':1}
		session 					= self.client.session
		session['first_form_data'] 	= first_form_data
		session.save()

		# Exercise test
		response = self.client.post(reverse('web_signup_second_form'), data={'username':'ibrahem', 'first_name':'ibrahem', 'last_name':'amer', 'email':'ibrahem@hotmail.com', 'password':123, 'password_confirm':123})


		# Assert test
		# 404 due to get_object_or_404, and database isn't populated.
		self.assertEqual(404, response.status_code)
		