from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User

class Topic(models.Model):
	# Helper variables
	topic_name_validator 	= RegexValidator(r'^[a-zA-Z][a-zA-Z0-9]*([ ]?[a-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')
	term_choices 			= [(1, 'First term'), (2, 'Second term'), (3, 'Summer')]

	# Class attributes
	name 		= models.CharField(max_length = 200, validators = [topic_name_validator])
	desc 		= models.CharField(max_length = 400)
	term 		= models.PositiveIntegerField(choices = term_choices)
	weeks		= models.PositiveIntegerField(default = 0)
	department 	= models.ForeignKey('users.Department', related_name = 'topics', on_delete = models.CASCADE)
	faculty 	= models.ForeignKey('users.Faculty', related_name = 'topics', on_delete = models.CASCADE, null = True)
	# Professors -> A list of associated professors for this topic.
	# Table -> A foriegn key that points to the table associated with this topic.
	# Lectures -> A list of materials that represents all primary content for the topic.
	# Contributions -> A list of materials that represents all secondary content for the topic.	
	
	def __str__(self):
		return self.name

	def clean(self):
		super(Topic, self).clean()
		if Topic.objects.filter(name = self.name).exclude(pk = self.pk).exists():
			raise ValidationError('Topic already exists.')

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
	    try:
	    	return user_obj.profile.topics.all()
	    except AttributeError:
	    	from users.models import UserProfile
	    	UserProfile.make_form_new_profile(user_obj)
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

	@classmethod
	def get_topics_choices(cls, user_obj):
		"""
		Accepts User, returns a list of all available topics with format --> {dep1:ListOfTopics, dep2:ListOfTopics, ..}
		"""
		results = {}

		# Returns topics that matches user faculty. 
		topics 	= Topic.objects.filter(faculty = user_obj.profile.faculty).all()
		# Grouping topics query by each department in user's faculty. 
		for dep in user_obj.profile.faculty.departments.all().order_by('name'):
			# Select from topics query topics that hold the same department id of current dep. 
			results[dep.name] = [candidate_topic for candidate_topic in topics if candidate_topic.department_id == dep.id]

		return results

	@classmethod
	def update_topics(cls, request, user_topics):
		"""
		Accepts ids of topics, validates them and update user's own topics to the queryset. 
		"""
		# Validating existence of each topic, pass if one of them doesn't exist.
		try:
			topics = Topic.objects.filter(id__in = user_topics)
		except Topic.DoesNotExist:
			pass

		if not topics:
			return False
		else:
			request.user.profile.topics = user_topics
			return True		


class Material(models.Model):
	# Helper attributes
	term_choices = [(1, 'First term'), (2, 'Second term'), (3, 'Summer')]
	type_choices = [(1, 'Lecture'), (2, 'Asset')]

	# Model Validator
	material_name_validator 	= RegexValidator(r'^[a-zA-Z][a-zA-Z0-9]*([ ]?[a-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.') 
	content_min_len_validator	= MinLengthValidator(50, 'Material Description should be more than 50 characters.')

	# Fields
	name 			= models.CharField(max_length = 200, validators = [material_name_validator], default = "N/A")
	content			= models.CharField(max_length = 500, validators = [content_min_len_validator])
	link 			= models.URLField(unique = True)
	year 			= models.DateField()
	term 			= models.PositiveIntegerField(choices = term_choices)
	content_type	= models.PositiveIntegerField(choices = type_choices)
	week_number 	= models.PositiveIntegerField()
	user 			= models.ForeignKey(User, related_name = 'primary_materials', on_delete = models.CASCADE)
	topic 			= models.ForeignKey('Topic', related_name = 'primary_materials', on_delete = models.CASCADE)
	# professor 	= foreignkey to professor

	def __str__(self):
		return self.name

	def clean(self):

		# Validates that week number associated with materials is real week number.
		try:
			if self.week_number not in range(self.topic.weeks):
				raise ValidationError('Week number is not found.')
		except ObjectDoesNotExist:
			# RelatedObject handler.
			self.week_number = 0


	# Material's methods
	@classmethod
	def get_department_materials(cls, department):
	    """
	    Returns list of materials that assoicate to specific departmnet. 
	    """
	    return 

	@classmethod
	def get_year_materials(cls, year, term = None):
	    """
	    Retruns list of materials that assoicate to specific year within specific term if term provided, All 3 terms otherwise.
	    """
	    return 

	@classmethod
	def get_prof_materials(cls, professor, term = None):
	    """
	    Returns list of materials that assoicate to specific professor in current year within specific term or all 3 terms. 
	    """
	    return

	def make_pdf_link(self):
		"""
		Generates the permalink to pdf file that will be used to display the file.
		"""
		return









