import datetime
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, validate_comma_separated_integer_list
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from cms.validators import GeneralCMSValidator

class Topic(models.Model):
	# Helper variables
	term_choices 			= [(1, 'First term'), (2, 'Second term'), (3, 'Summer')]

	# Class attributes
	name 		= models.CharField(max_length = 200, validators = [GeneralCMSValidator.name_validator])
	desc 		= models.CharField(max_length = 400)
	term 		= models.PositiveIntegerField(choices = term_choices)
	weeks		= models.PositiveIntegerField(default = 0)
	department 	= models.ForeignKey('users.Department', related_name = 'topics', on_delete = models.CASCADE)
	faculty 	= models.ForeignKey('users.Faculty', related_name = 'topics', on_delete = models.CASCADE, null = True)
	professors 	= models.ManyToManyField('Professor', related_name = 'topics')
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
	type_choices = [(1, 'Lecture'), (2, 'Asset'), (3, 'Task')]

	# Model Validator
	content_min_len_validator	= MinLengthValidator(50, 'Material Description should be more than 50 characters.')

	# Fields
	name 			= models.CharField(max_length = 200, validators = [GeneralCMSValidator.name_validator], default = "N/A")
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

	# Model-level validation
	def clean(self):

		# Validates that week number associated with materials is real week number.
		try:
			if self.week_number not in range(self.topic.weeks):
				raise ValidationError('Week number is not found.')
		except ObjectDoesNotExist:
			# RelatedObject handler.
			self.week_number = 0

        # Validate that user has an access to add material to topic.
		try:
			if self.user.profile.department.id != self.topic.department.id:
				raise ValidationError("Access denied.")
		except (AttributeError, ObjectDoesNotExist):
			raise ValidationError("Invalid User or Topic.")



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



class Task(Material):

	# Additional fields.
	deadline = models.DateField()


	# Model-level validation
	def clean(self):
		
		# Validate that deadline is not a passed date. 
		now = datetime.date.today()
		date_difference = self.deadline - now
		if date_difference.days <= 3:
			raise ValidationError('Deadline date should be 3 days ahead at least.')

	# Task methods.
	@classmethod
	def get_closest_tasks(cls, request):
	    """
	    Returns tasks whose deadlines occurs 3 days from now. 
	    """
	    now 		= datetime.date.today()
	    days_limit 	= datetime.timedelta(days = 4) 
	    return Task.objects.filter(topic__in = request.user.profile.topics.all(), deadline__range = (now, now+days_limit))


class Professor(models.Model):

	# Attributes
	name 	= models.CharField(max_length = 200, validators = [GeneralCMSValidator.name_validator], default = "N/A")
	faculty = models.ForeignKey('users.Faculty', related_name = 'professors', on_delete = models.CASCADE)
	bio 	= models.TextField(null = True, blank = True)
	picture = models.ImageField(default = 'doctor.jpg')
	email 	= models.EmailField(null = True, blank = True)
	website = models.URLField(null = True, blank = True)
	linkedn = models.URLField(null = True, blank = True)


	def __str__(self):
		return self.name


class Table(models.Model):
	"""Contains the basic components for building a table."""

	# Helopers
	days={
			0: 'Sat',
			1: 'Sun',
			2: 'Mon',
			3: 'Tue',
			4: 'Wen',
			5: 'Thu',
			6: 'Fri',
		}

	# Attributes
	topics = models.CharField(max_length = 200)
	places = models.CharField(max_length = 200)
	off_days = models.CharField(
		max_length = 200,
		validators=[validate_comma_separated_integer_list]
	)
	json = models.CharField(max_length = 200)

	# Meta
	class Meta:
		abstract = True

	# Methods
	def setjson(self):
		"""Concatenates topics and places into dict: {day: {period: {topic: 'topic', place: 'place'}}}"""

		table = {}
		for day in range(7):
			day_index = self.days[day]
			table[day_index] = {}
			for period in range(6):
				table[day_index][period] = {}
				table[day_index][period]['topic'] = self.topics[day][period]
				table[day_index][period]['place'] = self.places[day][period]
		self.json = str(table)


class TopicTable(Table):
	"""Manages the time table for each topic"""

	# Attributes
	topic = models.OneToOneField(
		Topic,
		on_delete=models.CASCADE,
		related_name='table'
	)
	

