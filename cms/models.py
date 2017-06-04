from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError 

class Topic(models.Model):
	# Helper variables
	topic_name_validator 	= RegexValidator(r'^[a-zA-Z][a-zA-Z0-9]*([ ]?[a-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')
	term_choices 			= [(1, 'First term'), (2, 'Second term'), (3, 'Summer')]

	# Class attributes
	name 		= models.CharField(max_length = 200, validators = [topic_name_validator])
	desc 		= models.CharField(max_length = 400)
	term 		= models.PositiveIntegerField(choices = term_choices)
	department 	= models.ForeignKey('users.Department', related_name = 'topics', on_delete = models.CASCADE)
	# Professors -> A list of associated professors for this topic.
	# Table -> A foriegn key that points to the table associated with this topic.
	# Lectures -> A list of materials that represents all primary content for the topic.
	# Contributions -> A list of materials that represents all secondary content for the topic.	

	def clean(self):
		if Topic.objects.filter(name = self.name).exists():
			raise ValidationError('Topic already exists.')

	def __str__(self):
		return self.name

class TopicNav(object):
	"""
	TopicNav is used in navbar and menus, hold information about each topic: name, link are most important. 
	"""
	def __init__(self, name, pk, dep_id):
		super(TopicNav, self).__init__()
		self.name 	= name
		self.pk 	= pk
		self.dep 	= dep_id
		self.link 	= self.make_topic_link()

	def __iter__(self):
		return self

	def make_topic_link(self):
		"""
		Creates topic link. Return visitable link. 
		"""
		return '/'+str(self.dep)+'/'+str(self.pk)


class UserTopics(object):
	"""
	Contains the methods meant to organize user interaction with topics. 
	"""

	@classmethod
	def get_user_topics(cls, user_obj):
	    """
	    Returns list of topics that user has access to. 
	    """
	    return user_obj.profile.topics.all()

	@classmethod
	def get_user_topics_nav(cls, user_obj):
		"""
        Returns list of TopicNav objects that user has access to. 
		"""
		nav_list = []

		topics 	= cls.get_user_topics(user_obj)
		if topics:
			for topic in topics:
				nav_topic = TopicNav(topic.name, topic.id, topic.department.id)
				nav_list.append(nav_topic)
		return nav_list

