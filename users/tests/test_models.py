from django.core.urlresolvers import resolve
from django.urls import reverse
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from unittest import skip
from users.views import home_visitor, display_signup
from users.models import University, Faculty, Department
from users.forms import SignupForm, UserSignUpForm

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
		self.fail('write me!')
		# Exercise test
		# Assert test
		