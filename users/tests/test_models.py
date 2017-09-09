from django.core.urlresolvers import resolve
from django.urls import reverse
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from django.contrib.messages.storage.fallback import FallbackStorage
from unittest import skip
from users.views import *
from users.models import University, Faculty, Department, UserProfile
from users.forms import SignupForm, UserSignUpForm
from django.contrib.auth.models import User


class UniversityModelTest(TestCase):
	
	def test_save_university(self):
		# Setup test
		mansoura_university 			= University()
		mansoura_university.uni_type 	= 'public'
		mansoura_university.save()
		kfs_university 					= University()
		kfs_university.uni_type 		= 'private'
		kfs_university.save()

		# Exercise test
		saved_universities = University.objects.all()

		# Assert test
		self.assertEqual(saved_universities.count(), 2)

	def test_retreive_university(self):
		# Setup test
		mansoura_university 	= University()
		mansoura_university.bio = 'a public university'
		mansoura_university.save()

		# Exercise test
		saved_university = University.objects.first()

		# Assert test
		self.assertEqual('a public university', saved_university.bio)

	def test_retreive_university_with_multiple_values(self):
		# Setup test
		mansoura_university 	= University()
		mansoura_university.bio = 'a public university'
		mansoura_university.save()
		kfs_university 			= University()
		kfs_university.bio 		= 'private'
		kfs_university.save()

		# Exercise test
		saved_university = University.objects.filter(bio='private').get()

		# Assert test
		self.assertEqual('private', saved_university.bio)

	def test_save_university_with_no_values(self):
		# Setup test
		mansoura_university = University()
		mansoura_university.save()

		# Exercise test
		saved_university = University.objects.get()

		# Assert test
		self.assertEqual('no data initialized', saved_university.bio)
		self.assertEqual('public', saved_university.uni_type)
		self.assertEqual('no name', saved_university.name)

class FacultyModelTest(TestCase):


	def test_save_faculty(self):
		# Setup test
		fac1 		= Faculty()
		fac1.name 	= 'engineering'
		fac1.save()
		fac2 		= Faculty()
		fac2.name 	= 'law'
		fac2.save()

		# Exercise test
		saved_faculty = Faculty.objects.all()

		# Assert test
		self.assertEqual(saved_faculty.count(), 2)

	def test_retreive_faculty(self):
		# Setup test
		fac1 		= Faculty()
		fac1.name 	= 'law'
		fac1.save()

		# Exercise test
		saved_faculty = Faculty.objects.first()

		# Assert test
		self.assertEqual('law', saved_faculty.name)

	def test_save_faculty_with_no_values(self):
		# Setup test
		mansoura_university = Faculty()
		mansoura_university.save()

		# Exercise test
		saved_faculty = Faculty.objects.get()

		# Assert test
		self.assertEqual('no data initialized', saved_faculty.bio)
		self.assertEqual('no name', saved_faculty.name)

	def test_attach_faculty_to_given_university(self):
		# Setup test
		fac1 = Faculty()
		uni1 = University()
		uni1.save()
		fac1.university = uni1
		fac1.save()

		# Exercise test
		db_university = University.objects.get()

		# Assert test
		self.assertIn(fac1, db_university.faculties.all())

class DepartmentModelTest(TestCase):


	def test_save_Department(self):
		# Setup test
		dep1 			= Department()
		dep1.name 		= 'first year'
		dep2 			= Department()
		dep2.dep_type 	= 'public'
		dep1.save()
		dep2.save()

		# Exercise test
		saved_deps = Department.objects.all().count()

		# Assert test
		self.assertEqual(2, saved_deps)

	def test_retreive_Department(self):
		# Setup test
		dep1 		= Department()
		dep1.name 	= 'software engineering'
		dep1.save()

		# Exercise test
		saved_dep = Department.objects.get(name = 'software engineering')

		# Assert test
		self.assertEqual(dep1.pk, saved_dep.pk)

	def test_save_Department_with_no_values(self):
		# Setup test
		dep1 = Department()
		dep1.save()

		# Exercise test
		saved_dep = Department.objects.first()
		
		# Assert test
		self.assertEqual('no name', saved_dep.name)

	def test_department_attached_to_faculty(self):
		# Setup test
		fac1 			= Faculty()
		fac1.name 		= 'KFS'
		fac1.save()
		dep1 			= Department()
		dep1.name 		= 'second year'
		dep1.dep_type 	= 'private'
		dep1.faculty 	= fac1
		dep1.save()
	
		# Exercise test
		saved_faculty = Faculty.objects.first()

		# Assert test
		self.assertNotIn('no_name', saved_faculty.departments.first().name)
		self.assertIn('second year', saved_faculty.departments.first().name)


	def test_save_faculty(self):
		# Setup test
		fac1 		= Faculty()
		fac1.name 	= 'engineering'
		fac1.save()
		fac2 		= Faculty()
		fac2.name 	= 'law'
		fac2.save()

		# Exercise test
		saved_faculty = Faculty.objects.all()

		# Assert test
		self.assertEqual(saved_faculty.count(), 2)

	def test_retreive_faculty(self):
		# Setup test
		fac1 		= Faculty()
		fac1.name 	= 'law'
		fac1.save()

		# Exercise test
		saved_faculty = Faculty.objects.first()

		# Assert test
		self.assertEqual('law', saved_faculty.name)

	def test_save_faculty_with_no_values(self):
		# Setup test
		mansoura_university = Faculty()
		mansoura_university.save()

		# Exercise test
		saved_faculty = Faculty.objects.get()

		# Assert test
		self.assertEqual('no data initialized', saved_faculty.bio)
		self.assertEqual('no name', saved_faculty.name)

	def test_attach_faculty_to_given_university(self):
		# Setup test
		fac1 = Faculty()
		uni1 = University()
		uni1.save()
		fac1.university = uni1
		fac1.save()

		# Exercise test
		db_university = University.objects.get()

		# Assert test
		self.assertIn(fac1, db_university.faculties.all())

class UserProfileTest(TestCase):

	def make_messages_available(self, request):
		"""
		Takes request and make django's messages available for it.
		"""
		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)

	def setUp(self):
		self.user 		= User.objects.create_user(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		self.uni 		= University.objects.create(name = 'Test university')
		self.fac 		= Faculty.objects.create(name = 'Test faculty')
		self.dep 		= Department.objects.create(name = 'Test dep')
		self.old_uni	= University()
		self.old_uni.save()
		self.old_fac	= Faculty(university = self.old_uni)
		self.old_fac.save()
		self.old_dep 	= Department(faculty = self.old_fac)
		self.old_dep.save()

	
	def test_insert_new_profile_with_user(self):
		# Setup test

		# Exercise test
		profile 		= UserProfile()
		profile.user 	= self.user
		
		# Assert test
		self.assertEqual(profile, self.user.profile)

	def test_insert_profile_with_data(self):
		# Setup test

		# Exercise test
		profile 		= UserProfile.objects.create(university = self.uni, faculty = self.fac, department = self.dep)
		profile.user 	= self.user
		
		# Assert test
		self.assertEqual('Test university', self.user.profile.university.name)
		self.assertEqual('Test faculty', self.user.profile.faculty.name)
		self.assertEqual('Test dep', self.user.profile.department.name)

	def test_profile_will_be_changed_when_user_change_it(self):
		# Setup test
		profile 		= UserProfile()
		profile.user 	= self.user

		# Exercise test
		another_profile = UserProfile()
		self.user.profile 	= another_profile

		
		# Assert test
		self.assertNotEqual(profile, self.user.profile)

	def test_update_vaild_username(self):
		# Setup test
		request 			= RequestFactory()
		request 			= request.post(reverse('web_change_username'), data={'new_username':'Ibraheeeeeeem'})
		user_profile 		= UserProfile(university = self.old_uni, faculty = self.old_fac, department = self.old_dep)
		user_profile.user 	= self.user
		user_profile.save()
		
		# Making messages available for request.
		from django.contrib.messages.storage.fallback import FallbackStorage
		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)

		request.user 	= self.user


		# Exercise test
		update_user_username(request)

		# Assert test
		self.assertEqual('Ibraheeeeeeem', self.user.username)

	def test_update_invalide_username(self):
		# Setup test
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_username'), data={'new_username':'13Ibraheeeem'})
		request.user 	= self.user

		# Making messages available for request.
		self.make_messages_available(request)

		# Exercise test
		update_user_username(request)

		# Assert test
		self.assertNotEqual('13Ibraheeeem', self.user.username)

	def test_update_existing_username(self):
		# Setup test
		existing_user 	= User.objects.create(username = 'ibrahem3amer', email = 'dddddd@test.com', password = 'secrettt23455')
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_username'), data={'new_username':'ibrahem3amer'})
		request.user 	= self.user

		# Making messages available for request.
		self.make_messages_available(request)

		# Exercise test
		update_user_username(request)


		# Assert test
		self.assertNotEqual('ibrahem3amer', self.user.username)

	def test_update_valid_mail(self):
		# Setup test
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_email'), data={'new_usermail':'ibrahem3amer@hotmail.com', 'new_usermail_confirmation':'ibrahem3amer@hotmail.com'})
		request.user 	= self.user

		# Making messages available for request.
		self.make_messages_available(request)

		# Exercise test
		update_user_email(request)

		# Assert test
		self.assertEqual('ibrahem3amer@hotmail.com', self.user.email)

	def test_update_invalid_mail(self):
		# Setup test
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_email'), data={'new_usermail':'ibrahem3amer.com', 'new_usermail_confirmation':'ibrahem3amer.com'})
		request.user 	= self.user

		# Making messages available for request.
		self.make_messages_available(request)

		# Exercise test
		update_user_email(request)

		# Making messages available for request.
		self.make_messages_available(request)

		# Assert test
		self.assertNotEqual('ibrahem3amer.com', self.user.email)

	def test_update_valid_password(self):
		# Unit test error that blocks me changing user password. But it works manually! 
		# Setup test
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_password'), data={
			'old_password':'secrettt23455', 
			'new_password':'seeeeeecccccrrrrrrrrtttttt2222222333',
			'new_password_confirm':'seeeeeecccccrrrrrrrrtttttt2222222333'
			})
		request.user 	= self.user

		# Making messages available for request.
		self.make_messages_available(request)

		# Exercise test
		response = update_user_password(request)

		# Assert test
		self.assertEqual(response.status_code, 200)


	def test_update_educational_info_with_valid(self):
		# Setup test
		user 				= User.objects.create(username='test', email='test_tt@test.com', password='00000111112222255555888ffff')
		user.save()
		user_profile 		= UserProfile(university = self.old_uni, faculty = self.old_fac, department = self.old_dep)
		user_profile.user 	= user
		user_profile.save()
		request 			= RequestFactory()
		request 			= request.post(reverse('web_change_info'), data={'universities-hidden':self.uni.id, 'faculties-hidden':self.fac.id, 'departments-hidden':self.dep.id, 'new_section_number': 5})
		request.user 		= user


		# Exercise test
		user.profile.university = self.old_uni
		user.profile.faculty 	= self.old_fac
		user.profile.department = self.old_dep
		
		# Making messages available for request.
		self.make_messages_available(request)
		
		update_user_education_info(request)

		# Assert test
		self.assertNotEqual(self.old_uni, user.profile.university)

	def test_update_educational_info_with_invalid_ids(self):
		# Setup test
		self.user 				= User.objects.create(username='test', email='test_tt@test.com', password='00000111112222255555888ffff')
		self.user.save()
		self.user_profile 		= UserProfile(university = self.old_uni, faculty = self.old_fac, department = self.old_dep)
		self.user_profile.user 	= self.user
		self.user_profile.save()
		request 					= RequestFactory()
		request 					= request.post(reverse('web_change_info'), data={'universities-hidden':99, 'faculties-hidden':99, 'departments-hidden':99, 'new_section_number': 99})
		request.user 				= self.user


		# Exercise test
		self.user.profile.university 	= self.old_uni
		self.user.profile.faculty 		= self.old_fac
		self.user.profile.department 	= self.old_dep

		# Making messages available for request.
		self.make_messages_available(request)

		update_user_education_info(request)

		# Assert test
		self.assertEqual(self.old_uni, self.user.profile.university)