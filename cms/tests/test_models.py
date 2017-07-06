from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError 
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from unittest import skip
from cms.models import Topic, UserTopics, Material
from cms.views import update_user_topics
from users.models import Department, UserProfile, Faculty

class TopicTest(TestCase):
	def test_add_valid_topic(self):
		# Setup test
		dep = Department.objects.create()
		t 	= Topic.objects.create(name = 'test topic with spaces', desc = 'ddddd', term = 1, department = dep)

		# Exercise test
		query = Topic.objects.get()

		# Assert test
		self.assertEqual('test topic with spaces', query.name)
		self.assertEqual(dep, query.department)

	def test_add_invalid_topic_name(self):
		# Setup test
		dep = Department.objects.create()
		t 	= Topic.objects.create(name = '123', desc = 'ddddd', term = 1, department = dep)
		
		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, t.clean())

	def test_add_repeated_topic_name(self):
		# Setup test
		dep = Department.objects.create()
		t 	= Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = dep)
		t2 	= Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = dep)
		
		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, t2.clean)

class UserTopicsTest(TestCase):
	def make_messages_available(self, request):
		"""
		Takes request and make django's messages available for it.
		"""
		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)

	def setUp(self):
		self.user 			= User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		self.fac 			= Faculty.objects.create()
		self.dep 			= Department.objects.create(faculty = self.fac)
		self.user.profile 	= UserProfile.objects.create(department = self.dep, faculty = self.fac)
		self.topic 			= Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = self.dep)

	def test_return_user_topics(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)

		# Exercise test
		topics = UserTopics.get_user_topics(self.user)
		
		# Assert test
		self.assertEqual(len(topics), 1)
		self.assertEqual(topics[0], self.topic)

	def test_return_user_topics_with_no_profile(self):
		# Setup test	
		user2 = User.objects.create(username = 'test_2', email = 'tesssst@test.com', password = 'secrettt23455')

		# Exercise test
		topics = UserTopics.get_user_topics(user2)
		
		# Assert test
		self.assertEqual(len(topics), 0)

	def test_return_available_topics(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		dep2 = Department.objects.create(name = "test_dep", faculty = self.fac)
		
		# Exercise test
		topics 	= UserTopics.get_topics_choices(self.user)
		
		# Assert test
		self.assertIn(self.topic.department.name, topics)
		# Assure that results include all departments within same faculty.
		self.assertIn(dep2.name, topics)

	def test_update_topics_with_correct_ids(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		new_topic 	= []
		t1 			= Topic.objects.create(name = 'topic_new_2', desc = 'ddddd', term = 1, department = self.dep)
		new_topic.append(t1.id)
		t2 			= Topic.objects.create(name = 'topic_new_3', desc = 'ddddd', term = 2, department = self.dep)
		new_topic.append(t2.id)
		t3 			= Topic.objects.create(name = 'topic_new_4', desc = 'ddddd', term = 3, department = self.dep)
		new_topic.append(t3.id)


		# Exercise test
		request 		= RequestFactory()
		request 		= request.post(reverse('update_user_topics'), data = {'chosen_list[]':new_topic})
		request.user 	= self.user
		
		# Making messages available for request.
		self.make_messages_available(request)

		update_user_topics(request)

		
		# Assert test
		self.assertEqual(self.user.profile.topics.all().count(), 3)

	def test_update_topics_with_empty_list(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		new_topic 	= []


		# Exercise test
		request 		= RequestFactory()
		request 		= request.post(reverse('update_user_topics'), data = {'chosen_list[]':new_topic})
		request.user 	= self.user
		
		# Making messages available for request.
		self.make_messages_available(request)

		update_user_topics(request)

		
		# Assert test
		self.assertEqual(self.user.profile.topics.all().count(), 1)

	def test_update_topics_with_all_incorrect_ids(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		new_topic 	= [990, 1200, 1510]


		# Exercise test
		request 		= RequestFactory()
		request 		= request.post(reverse('update_user_topics'), data = {'chosen_list[]':new_topic})
		request.user 	= self.user

		# Making messages available for request.
		self.make_messages_available(request)

		update_user_topics(request)

		
		# Assert test
		self.assertEqual(self.user.profile.topics.all().count(), 1)

	def test_update_topics_with_half_correct_half_incorrect(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		new_topic 	= []
		t1 			= Topic.objects.create(name = 'topic_new_2', desc = 'ddddd', term = 1, department = self.dep)
		new_topic.append(t1.id)
		t2 			= Topic.objects.create(name = 'topic_new_3', desc = 'ddddd', term = 2, department = self.dep)
		new_topic.append(t2.id)
		t3 			= Topic.objects.create(name = 'topic_new_4', desc = 'ddddd', term = 3, department = self.dep)
		new_topic.append(t3.id)
		new_topic.append(990)
		new_topic.append(5300)
		new_topic.append(8000)


		# Exercise test
		request 		= RequestFactory()
		request 		= request.post(reverse('update_user_topics'), data = {'chosen_list[]':new_topic})
		request.user 	= self.user

		# Making messages available for request.
		self.make_messages_available(request)

		update_user_topics(request)

		
		# Assert test
		self.assertEqual(self.user.profile.topics.all().count(), 3)

	def test_update_topics_with_correct_ids_that_user_cannot_access(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		another_faculty 				= Faculty.objects.create()
		another_dep_user_cannot_access 	= Department.objects.create(faculty = another_faculty)
		new_topic 	= []
		t1 			= Topic.objects.create(name = 'topic_new_2', desc = 'ddddd', term = 1, department = another_dep_user_cannot_access)
		new_topic.append(t1.id)
		t2 			= Topic.objects.create(name = 'topic_new_3', desc = 'ddddd', term = 2, department = another_dep_user_cannot_access)
		new_topic.append(t2.id)
		t3 			= Topic.objects.create(name = 'topic_new_4', desc = 'ddddd', term = 3, department = another_dep_user_cannot_access)
		new_topic.append(t3.id)


		# Exercise test
		request 		= RequestFactory()
		request 		= request.post(reverse('update_user_topics'), data = {'chosen_list[]':new_topic})
		request.user 	= self.user
		
		# Making messages available for request.
		self.make_messages_available(request)

		update_user_topics(request)

		
		# Assert test
		self.assertEqual(self.user.profile.topics.all().count(), 1)

class MaterialTest(TestCase):
	def setUp(self):
		self.dep 		= Department.objects.create()
		self.topic 		= Topic.objects.create(name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
		self.user 		= User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f')
		self.material 	= Material.objects.create(
				name 			= 'test_material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.google.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 1,
				user 			= self.user,
				topic 			= self.topic
			)

	def test_add_material(self):
		# Setup test
		material_test = Material.objects.create(
				name 			= 'test_material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.godogle.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 1,
				user 			= self.user,
				topic 			= self.topic
			)

		# Exercise test
		materials_in_db = Material.objects.latest('id')
		
		# Assert test
		self.assertEqual(material_test, materials_in_db)

	def test_add_material_with_invalid_name(self):
		# Setup test
		material_test = Material.objects.create(
				name 			= '123material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.gofogle.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 0,
				user 			= self.user,
				topic 			= self.topic
			)

		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: material_test.full_clean())

	def test_add_material_with_empty_content(self):
		# Setup test
		material_test = Material.objects.create(
				name 			= 'material',
				content 		= '',
				link 			= 'http://www.docs.googlce.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 0,
				user 			= self.user,
				topic 			= self.topic
			)

		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: material_test.full_clean())

	def test_add_material_with_content_less_than_50(self):
		# Setup test
		material_test = Material.objects.create(
				name 			= 'material',
				content 		= 'f',
				link 			= 'http://www.docs.gosogle.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 2,
				user 			= self.user,
				topic 			= self.topic
			)

		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: material_test.full_clean())

	def test_add_material_with_week_number_that_doesnot_exist(self):
		# Setup test
		material_test = Material.objects.create(
				name 			= 'material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.googssle.com',
				year 			= '2123-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 99,
				user 			= self.user,
				topic 			= self.topic
			)

		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: material_test.full_clean())		