from django.core.urlresolvers import resolve
from django.urls import reverse
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from unittest import skip
from users.views import home_visitor, display_signup
from users.models import University, Faculty, Department
from users.forms import SignupForm, UserSignUpForm

class user_sign_up(TestCase):
	def setUp(self):
		self.signup_module = self.client.get(reverse('web_signup'))

	def test_user_submit_first_form(self):
		# Setup test
		first_stage_response = self.client.get(reverse('web_signup_second_form'), data ={'selected_university':'1', 'selected_faculty':'1', 'selected_department':'1'})

		# Exercise test
		# Assert test
		self.assertEqual(200, first_stage_response.status_code)
		self.assertTemplateUsed(first_stage_response, 'signup_second_form.html')

	@skip
	def test_second_form_with_empty_values(self):
		# Setup test
		form = self.client.get(reverse('web_signup_second_form'))

		# Exercise test
		expected_error 	= 'You should select your university, faculty and department.'
		erorr 			= form.context['error']
		# Assert test
		self.assertEqual(expected_error, error)
