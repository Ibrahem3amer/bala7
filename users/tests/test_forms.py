from django.core.urlresolvers import resolve
from django.urls import reverse
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from unittest import skip
from users.views import home_visitor, display_signup
from users.models import University, Faculty, Department
from users.forms import SignupForm, UserSignUpForm
from django.contrib.auth.models import User


class signup_form_test(TestCase):
	def test_user_submits_valid_form(self):
		# Setup test
		u = User()
		u.username = 'waaaaeeel'
		u.email = 'waeeel@hotmail.com'
		data = {'username':u.username, 'email':u.email, 'password':'123', 'password_confirm':'123'}
		
		# Exercise test
		form = UserSignUpForm(data=data)
		
		# Assert test
		self.assertTrue(form.is_valid())

	def test_users_submits_invalid_username(self):
		# Setup test
		u = User()
		u.username = '123'
		u.email = 'ibrahem3amer@fff.com'
		data = {'username':u.username, 'email':u.email, 'password':'123', 'password_confirm':'123'}

		# Exercise test
		form = UserSignUpForm(data=data)
		
		# Assert test
		self.assertFalse(form.is_valid())
		self.fail('invalid username cause failure in email validation as it check for key that is not true.')

	def test_users_submits_unmatched_password(self):
		# Setup test
		u = User()
		u.username = 'iige13'
		u.email = 'ibrahem3amer@fff.com'
		data = {'username':u.username, 'email':u.email, 'password':'555', 'password_confirm':'123'}
		
		# Exercise test
		form = UserSignUpForm(data=data)

		# Assert test
		self.assertFalse(form.is_valid())

	def test_password_strength(self):
		# Setup test
		self.fail('write me!')
		# Exercise test
		# Assert test