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
		data = {'username':u.username, 'email':u.email, 'password':'12345678abc', 'password_confirm':'12345678abc'}
		
		# Exercise test
		form = UserSignUpForm(data=data)
		
		# Assert test
		self.assertTrue(form.is_valid())

	def test_users_submits_invalid_username(self):
		# Setup test
		u = User()
		u.username = '123'
		u.email = 'ibrahem3amer@fff.com'
		data = {'username':u.username, 'email':u.email, 'password':'12345678abc', 'password_confirm':'12345678abc'}

		# Exercise test
		form = UserSignUpForm(data=data)
		
		# Assert test
		self.assertFalse(form.is_valid())

	def test_users_submits_arabic_username(self):
		# Setup test
		u = User()
		u.username = 'فارس'
		u.email = 'ibrahem3amer@fff.com'
		data = {'username':u.username, 'email':u.email, 'password':'12345678abc', 'password_confirm':'12345678abc'}

		# Exercise test
		form = UserSignUpForm(data=data)
		
		# Assert test
		self.assertTrue(form.is_valid())

	def test_users_submits_arabic_username_with_extended_letters(self):
		# Setup test
		u = User()
		u.username = 'فارس_الإسلام'
		u.email = 'ibrahem3amer@fff.com'
		data = {'username':u.username, 'email':u.email, 'password':'12345678abc', 'password_confirm':'12345678abc'}

		# Exercise test
		form = UserSignUpForm(data=data)
		
		# Assert test
		print(form.errors)
		self.assertTrue(form.is_valid())

	def test_users_submits_unmatched_password(self):
		# Setup test
		u = User()
		u.username = 'iige13'
		u.email = 'ibrahem3amer@fff.com'
		data = {'username':u.username, 'email':u.email, 'password':'12345678abc', 'password_confirm':'12345678bca'}
		
		# Exercise test
		form = UserSignUpForm(data=data)

		# Assert test
		self.assertFalse(form.is_valid())

	# Causes keyError exception because of the front-end validation that password should be 7 digits.
	def test_password_strength(self):
		# Setup test
		u = User()
		u.username = 'ibham'
		u.email = 'ibrahem3amer@ssss.com'
		data = {'username':u.username, 'email':u.email, 'password':'555', 'password_confirm':'555'}
		
		# Exercise test
		form = UserSignUpForm(data=data)

		# Assert test
		self.assertFalse(form.is_valid())

	def test_password_with_only_digits(self):
		# Setup test
		u = User()
		u.username = 'ibham'
		u.email = 'ibrahem3amer@ssss.com'
		data = {'username':u.username, 'email':u.email, 'password':'12345678', 'password_confirm':'12345678'}
		
		# Exercise test
		form = UserSignUpForm(data=data)

		# Assert test
		self.assertFalse(form.is_valid())

