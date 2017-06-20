from django.core.urlresolvers import resolve
from django.urls import reverse
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from unittest import skip
from users.views import home_visitor, display_signup
from users.models import University, Faculty, Department, UserProfile
from users.forms import SignupForm, UserSignUpForm
from django.contrib.auth.models import User

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



class signup_and_signin(TestCase):
	def setUp(self):
		self.old_uni 			= University()
		self.old_uni.save()
		self.old_fac			= Faculty(university = self.old_uni)
		self.old_fac.save()
		self.old_dep 			= Department(faculty = self.old_fac)
		self.old_dep.save()

	def test_signup_returns_correct_output(self):
		# Setup test
		response = self.client.get(reverse('web_signup'))

		# Exercise test
		# Assert test
		self.assertEqual(200, response.status_code)
		self.assertTemplateUsed(response, 'registration/signup.html')
	
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
		first_form_data 			= {'university':self.old_uni.id, 'faculty':self.old_fac.id, 'department':self.old_dep.id}
		session 					= self.client.session
		session['first_form_data'] 	= first_form_data
		session.save()

		# Exercise test
		response = self.client.post(reverse('web_signup_second_form'), data={'username':'test', 'first_name':'ibrahem', 'last_name':'amer', 'email':'ibrahem@hotmail.com', 'password':'12345678abc', 'password_confirm':'12345678abc'})


		# Assert test
		# Redirect user to homepage if success.
		self.assertEqual(302, response.status_code)

	def test_user_reach_signin(self):
		# Setup test
		response = self.client.get(reverse('login'))
		# Exercise test
		# Assert test
		self.assertEqual(200, response.status_code)

	def test_user_signout(self):
		# Setup test
		response = self.client.get(reverse('logout'))
		# Exercise test
		# Assert test
		self.assertEqual(200, response.status_code)

	def test_homeuser_redirect_without_login(self):
		# Setup test
		response = self.client.get(reverse('home_user'))
		# Exercise test
		# Assert test
		self.assertEqual(302, response.status_code)

	def test_homeuser_with_login(self):
		# Setup test
		user 				= User.objects.create(username='test', email='test_tt@test.com', password='00000111112222255555888ffff')
		user.save()
		user_profile 		= UserProfile(university = self.old_uni, faculty = self.old_fac, department = self.old_dep)
		user_profile.user 	= user
		user_profile.save()

		
		# Exercise test
		request = self.client.force_login(user)
		response = self.client.get(reverse('home_user'))

		# Assert test
		self.assertEqual(200, response.status_code)

	def test_profile_with_login(self):
		# Setup test
		user 				= User.objects.create(username='test', email='test_tt@test.com', password='00000111112222255555888ffff')
		user.save()
		user_profile 		= UserProfile(university = self.old_uni, faculty = self.old_fac, department = self.old_dep)
		user_profile.user 	= user
		user_profile.save()

		# Exercise test
		request = self.client.force_login(user)
		response = self.client.get(reverse('web_user_profile'))
		
		# Assert test
		self.assertEqual(200, response.status_code)

	def test_profile_without_login(self):
		# Setup test
		response = self.client.get(reverse('web_user_profile'))
		# Exercise test
		# Assert test
		self.assertEqual(302, response.status_code)

	def test_update_profile_username_without_login(self):
		# Setup test
		response = self.client.post(reverse('web_change_username'))
		# Exercise test
		# Assert test
		self.assertEqual(302, response.status_code)

	def test_update_profile_username_login(self):
		# Setup test
		user = User.objects.create(username='test', email='test_tt@test.com', password='00000111112222255555888ffff')

		# Exercise test
		request = self.client.force_login(user)
		response = self.client.get(reverse('web_change_username'), data = {'new_username': 'idfsfsdf'})
		
		# Assert test
		# 302 as it success and return to profile. 
		self.assertEqual(302, response.status_code)

	def test_update_email_without_login(self):
		# Setup test
		response = self.client.post(reverse('web_change_email'))
		# Exercise test
		# Assert test
		self.assertEqual(302, response.status_code)

	def test_update_password_without_login(self):
		# Setup test
		response = self.client.post(reverse('web_change_password'))
		# Exercise test
		# Assert test
		self.assertEqual(302, response.status_code)
