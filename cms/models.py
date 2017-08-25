import datetime
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import RegexValidator, MinLengthValidator, validate_comma_separated_integer_list
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from cms.validators import GeneralCMSValidator

TABLE_DAYS_LIST = [0, 1, 2, 3, 4, 5, 6]
TABLE_DAYS = 7
TABLE_PERIODS_LIST = [0, 1, 2, 3, 4, 5]
TABLE_PERIODS = 6

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

class MaterialBase(models.Model):
	# Helper attributes
	term_choices = [(1, 'First term'), (2, 'Second term'), (3, 'Summer')]
	type_choices = [(1, 'Lecture'), (2, 'Asset'), (3, 'Task')]

	# Model Validator
	content_min_len_validator	= MinLengthValidator(50, 'Material Description should be more than 50 characters.')

	# Fields
	name 			= models.CharField(max_length = 200, validators = [GeneralCMSValidator.name_validator], default = "N/A")
	content			= models.TextField(validators = [content_min_len_validator])
	link 			= models.URLField(unique = True)
	year 			= models.DateField()
	term 			= models.PositiveIntegerField(choices = term_choices)
	content_type	= models.PositiveIntegerField(choices = type_choices)
	week_number 	= models.PositiveIntegerField()

	class Meta:
		abstract = True

	def __str__(self):
		return self.name

	# Model-level validation
	def clean(self):

		# Validates that week number associated with materials is real week number.
		try:
			if self.week_number not in range(self.topic.weeks+1):
				raise ValidationError('Week number is not found.')
		except ObjectDoesNotExist:
			# RelatedObject handler.
			self.week_number = 0

        # Validate that user has an access to add material to topic.
		try:
			if self.topic not in self.user.profile.topics.all():
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


class Material(MaterialBase):

	user = models.ForeignKey(User, related_name = 'primary_materials', on_delete = models.CASCADE)
	topic = models.ForeignKey('Topic', related_name = 'primary_materials', on_delete = models.CASCADE)
	professor = models.ManyToManyField('Professor', related_name='primary_materials')

	# Model-level validation
	def clean(self):
		super(Material, self).clean()
		
		# Validate that user has an access to add material to topic.
		try:
			if self.topic not in self.user.profile.topics.all():
				raise ValidationError("Access denied.")
		except (AttributeError, ObjectDoesNotExist):
			raise ValidationError("Invalid User or Topic.")


class Exam(MaterialBase):

	# Additional fields.
	user = models.ForeignKey(User, related_name = 'exams', on_delete = models.CASCADE)
	topic = models.ForeignKey('Topic', related_name = 'exams', on_delete = models.CASCADE)
	professor = models.ManyToManyField('Professor', related_name='exams')

	# Model-level validation
	def clean(self):

		# Exams have no weeks, terms or type.
		self.week_number = 0
		self.term = 1
		self.content_type = 1

		# Validate that user has an access to add material to topic.
		try:
			if self.topic not in self.user.profile.topics.all():
				raise ValidationError("Access denied.")
		except (AttributeError, ObjectDoesNotExist):
			raise ValidationError("Invalid User or Topic.")

class Task(MaterialBase):

	# Additional fields.
	user = models.ForeignKey(User, related_name = 'primary_tasks', on_delete = models.CASCADE)
	topic = models.ForeignKey('Topic', related_name = 'primary_tasks', on_delete = models.CASCADE)
	professor = models.ManyToManyField('Professor', related_name='primary_tasks')
	deadline = models.DateField()


	# Model-level validation
	def clean(self):
		super(Task, self).clean()
		# Validate that user has an access to add material to topic.
		try:
			if self.topic not in self.user.profile.topics.all():
				raise ValidationError("Access denied.")
		except (AttributeError, ObjectDoesNotExist):
			raise ValidationError("Invalid User or Topic.")

		# Validate that deadline is not a passed date. 
		now = datetime.date.today()
		date_difference = self.deadline - now
		if date_difference.days <= 3:
			raise ValidationError('Deadline date should be 3 days ahead at least.')

	# Task methods.
	@classmethod
	def get_closest_tasks(cls, request):
		"""Returns tasks whose deadlines occurs 3 days from now."""
		from itertools import chain
		now = datetime.date.today()
		days_limit = datetime.timedelta(days = 4) 
		primary_tasks = Task.objects.filter(topic__in = request.user.profile.topics.all(), deadline__range = (now, now+days_limit))
		secondary_tasks = UserContribution.objects.filter(status=3, content_type=3, topic__in=request.user.profile.topics.all(), deadline__range=(now, now+days_limit))	
		return list(chain(primary_tasks, secondary_tasks))


class UserContribution(MaterialBase):
	
	# Helper attributes
	contribution_status = [(1, 'Pending'), (2, 'Rejected'), (3, 'Accepted')]

	# Additional fields.
	status = models.PositiveIntegerField(choices=contribution_status, default=1)
	supervisior_id = models.PositiveIntegerField(blank=True, default=0)
	deadline = models.DateField(blank=True, default=False)
	user = models.ForeignKey(User, related_name = 'secondary_materials', on_delete = models.CASCADE)
	topic = models.ForeignKey('Topic', related_name = 'secondary_materials', on_delete = models.CASCADE)
	professor = models.ManyToManyField('Professor', related_name='secondary_materials')

	# Model-level validation.
	def clean(self):
		super(UserContribution, self).clean()
		
		# Validate that user has an access to add material to topic.
		try:
			if self.topic not in self.user.profile.topics.all():
				raise ValidationError("Access denied.")
		except (AttributeError, ObjectDoesNotExist):
			raise ValidationError("Invalid User or Topic.")

		# Validate that deadline is not a passed date. 
		if self.content_type == 3 or self.content_type == '3':
			now = datetime.date.today()
			date_difference = self.deadline - now
			if date_difference.days <= 3:
				raise ValidationError('Deadline date should be 3 days ahead at least.')

	def __str__(self):
		return self.user.username + ' ' +self.name



class UserPost(models.Model):
	
	# Helpers 
	post_status = [(1, 'Pending'), (2, 'Rejected'), (3, 'Accepted')]

	# Attributes
	title = models.CharField(max_length=200, validators=[GeneralCMSValidator.name_validator], default="N/A")
	content = models.TextField()
	user = models.ForeignKey(User, related_name = 'posts', on_delete = models.CASCADE)
	topic = models.ForeignKey('Topic', related_name = 'posts', on_delete = models.CASCADE)
	status = models.PositiveIntegerField(choices=post_status, default=1)
	supervisior_id = models.PositiveIntegerField(blank=True, default=0)
	last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


class UserComment(models.Model):
	# Helpers
	comment_status = [(0, 'Blocked'), (1, 'Accepted')]

	# Attributes
	content = models.TextField()
	user = models.ForeignKey(User, related_name = 'comments', on_delete = models.CASCADE)
	post = models.ForeignKey('UserPost', related_name = 'comments', on_delete = models.CASCADE)
	status = models.PositiveIntegerField(choices=comment_status, default=1)
	last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username + ' -> ' +self.post.title


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
	topics = models.TextField()
	places = models.TextField()
	off_days = models.CharField(
		max_length = 200,
		validators=[validate_comma_separated_integer_list]
	)
	json = models.TextField()

	# Meta
	class Meta:
		abstract = True

	# Methods
	def set_final_table(self):
		"""Concatenates topics and places into one list."""

		table = [['']*TABLE_PERIODS for i in range(TABLE_DAYS)]
		topics = self.to_list(str(self.topics)) if type(self.topics) is not list else self.topics
		places = self.to_list(str(self.places)) if type(self.places) is not list else self.places

		for day in range(TABLE_DAYS):
			for period in range(TABLE_PERIODS):
				table[day][period] = topics[day][period] + ' @ ' + places[day][period]
		
		self.json = table 
		
		return table

	def to_list(self, str_attribute):
		"""Returns a list representation of topics attribute."""
		import ast
		try:
			list_representation = ast.literal_eval(str_attribute)
		except:
			list_representation = {}
		return list_representation

class TopicTable(Table):
	"""Manages the time table for each topic"""

	# Attributes
	topic = models.OneToOneField(
		Topic,
		on_delete=models.CASCADE,
		related_name='table'
	)

	def __str__(self):
		return self.topic.name + ' table'


class UserTable(Table):
	"""Holds user selections for table."""

	# Attributes
	user_profile = models.OneToOneField(
		'users.UserProfile',
		on_delete=models.CASCADE,
		related_name='table'
	)

	# Methods
	@classmethod
	def initiate_user_table(cls, choices):
		"""Takes user choices and forms a table."""
		user_table_topics = [['']*TABLE_PERIODS for i in range(TABLE_DAYS)]
		user_table_places = [['']*TABLE_PERIODS for i in range(TABLE_DAYS)]
		for choice in choices:
			# Split choice and populate user table.
			choice_arr = choice.split('_')
			if len(choice_arr) >= 3:
				topic_id, day, period = int(choice_arr[0]), int(choice_arr[1]), int(choice_arr[2])
				try:
					topic = Topic.objects.get(pk=topic_id)
					topic = get_object_or_404(Topic, pk=topic_id)
					table = topic.table.set_final_table()
					user_table_topics[day][period] += '@'+table[day][period]
					user_table_places[day][period] += '@'+table[day][period]
				except:
					continue

		return [user_table_topics, user_table_places]

	def __str__(self):
		return self.user_profile.user.username + ' table'


class DepartmentTable(object):
	"""Manages the available options of user's query."""
	
	# Attributes 
	user_topics = []
	department_topics = []
	available_topics = []
	professors = []


	# Methods
	def get_user_topics(self, user):
		"""Graps user choices of topics."""
		try:
			return user.profile.topics.all()
		except:
			# Profile doesn't exist.
			return []

	def get_dep_topics(self, user):
		"""Graps user's department topics."""
		try:
			return user.profile.department.topics.all()
		except:
			# Profile doesn't exist.
			return []

	def get_available_topics(self):
		"""Make the unioun of user_topics and dep_topics"""
		return list(set(self.department_topics).union(self.user_topics))

	def get_available_topics_professors(self):
		"""Returns a set of all availabe professors."""
		professors = []
		for topic in self.available_topics:
			try:
				for prof in topic.professors.all():
					professors.append(prof)
			except:
				# Topic or Professor doesn't exist 
				pass
		return list(set(professors))

	def query_table(self, user, topics, professors, periods, days):
		"""Queries table based on user specifications."""
		if topics:
			# Filter topics so that it matches user's input.
			self.available_topics = [topic for topic in self.available_topics if str(topic.id) in topics]
		
		if professors:
			# Filter each topic so that its professors should lay in user's input. 
			filtered_topics = []
			for topic in self.available_topics:
				for professor in topic.professors.all():
					if str(professor.id) in professors:
						filtered_topics.append(topic)
			self.available_topics = filtered_topics

		return self.filter_table(days, periods)

	def filter_table(self, days=None, periods=None):
		"""filter available topics based on days and periods."""
		table = [ [ [0] for k in range(20) ] for j in range(TABLE_PERIODS) for i in range(TABLE_DAYS) ]
		choices = []
		if self.available_topics:
			# Assign default value for days or periods if not provided.
			days = TABLE_DAYS_LIST if not days else days
			periods = TABLE_PERIODS_LIST if not periods else periods

			# Construct final table for each available topic. 
			# Populate another table with days and periods that matches user's input.
			for topic in self.available_topics:
				try:
					final_table = topic.table.set_final_table()
					for day in days:
						for period in periods:
							if len(final_table[int(day)][int(period)]) > 2:
								table[int(day)][int(period)].append(final_table[int(day)][int(period)])
								choices.append(str(topic.id)+'_'+str(day)+'_'+str(period))

				except ObjectDoesNotExist:
					# Topic has no table.

					continue
					
		return [table, choices]



	def __init__(self, user):
		super(DepartmentTable, self).__init__()
		self.user_topics = self.get_user_topics(user)
		self.department_topics = self.get_dep_topics(user)
		self.available_topics = self.get_available_topics()
		self.professors = self.get_available_topics_professors()
			
		
	

