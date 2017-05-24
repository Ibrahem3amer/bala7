from django.core.urlresolvers import resolve
from django.urls import reverse
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from unittest import skip
from users.views import *
from users.models import University, Faculty, Department, UserProfile
from users.forms import SignupForm, UserSignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


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
		self.assertEqual(1, saved_dep.id)

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
	
	def test_insert_new_profile_with_user(self):
		# Setup test
		user = User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')

		# Exercise test
		profile 		= UserProfile()
		profile.user 	= user
		
		# Assert test
		self.assertEqual(profile, user.profile)

	def test_insert_profile_with_data(self):
		# Setup test
		user 	= User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		uni 	= University.objects.create(name = 'Test university')
		fac 	= Faculty.objects.create(name = 'Test faculty')
		dep 	= Department.objects.create(name = 'Test dep')

		# Exercise test
		profile 		= UserProfile.objects.create(university = uni, faculty = fac, department = dep)
		profile.user 	= user
		
		# Assert test
		self.assertEqual('Test university', user.profile.university.name)
		self.assertEqual('Test faculty', user.profile.faculty.name)
		self.assertEqual('Test dep', user.profile.department.name)

	def test_profile_will_be_changed_when_user_change_it(self):
		# Setup test
		user = User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		profile 		= UserProfile()
		profile.user 	= user

		# Exercise test
		another_profile = UserProfile()
		user.profile 	= another_profile

		
		# Assert test
		self.assertNotEqual(profile, user.profile)

	def test_update_vaild_username(self):
		# Setup test
		user 			= User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_username'), data={'new_username':'Ibraheeeeeeem'})
		request.user 	= user


		# Exercise test
		update_user_username(request)

		# Assert test
		self.assertEqual('Ibraheeeeeeem', user.username)

	def test_update_invalide_username(self):
		# Setup test
		user 			= User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_username'), data={'new_username':'13Ibraheeeem'})
		request.user 	= user


		# Exercise test
		update_user_username(request)

		# Assert test
		self.assertNotEqual('13Ibraheeeem', user.username)

	def test_update_existing_username(self):
		# Setup test
		existing_user 	= User.objects.create(username = 'ibrahem3amer', email = 'dddddd@test.com', password = 'secrettt23455')
		user 			= User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_username'), data={'new_username':'ibrahem3amer'})
		request.user 	= user


		# Exercise test
		update_user_username(request)

		# Assert test
		self.assertNotEqual('ibrahem3amer', user.username)

	def test_update_valid_mail(self):
		# Setup test
		user 			= User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_email'), data={'new_usermail':'ibrahem3amer@hotmail.com', 'new_usermail_confirmation':'ibrahem3amer@hotmail.com'})
		request.user 	= user


		# Exercise test
		update_user_email(request)

		# Assert test
		self.assertEqual('ibrahem3amer@hotmail.com', user.email)

	def test_update_invalid_mail(self):
		# Setup test
		user 			= User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_email'), data={'new_usermail':'ibrahem3amer.com', 'new_usermail_confirmation':'ibrahem3amer.com'})
		request.user 	= user


		# Exercise test
		update_user_email(request)

		# Assert test
		self.assertNotEqual('ibrahem3amer.com', user.email)

	def test_update_valid_password(self):
		# Setup test
		user 			= User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		request 		= RequestFactory()
		request 		= request.post(reverse('web_change_password'), data={
			'old_password':'secrettt23455', 
			'new_password':'seeeeeecccccrrrrrrrrtttttt2222222333',
			'new_password_confirm':'seeeeeecccccrrrrrrrrtttttt2222222333'
			})
		request.user 	= user


		# Exercise test
		update_user_password(request)

		# Assert test
		self.fail('fix_me')
		self.assertTrue(check_password('seeeeeecccccrrrrrrrrtttttt2222222333', user.password))
