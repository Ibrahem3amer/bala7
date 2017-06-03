from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.core.exceptions import ValidationError 
from django.contrib.auth.models import User
from unittest import skip
from cms.models import Topic
from users.models import Department

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
		self.assertRaises(ValidationError, t.clean)

	def test_add_repeated_topic_name(self):
		# Setup test
		dep = Department.objects.create()
		t 	= Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = dep)
		t2 	= Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = dep)
		
		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, t2.clean)




