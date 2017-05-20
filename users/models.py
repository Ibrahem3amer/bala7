from django.db import models
from django.contrib.auth.models import User
from django.http import Http404


# Create your models here.
class Entity(models.Model):
	name 		= models.CharField(max_length = 100, default = 'no name')
	bio 		= models.CharField(max_length = 200, default = 'no data initialized')
	location 	= models.CharField(max_length = 200, default = 'no data initialized')
	headmaster 	= models.CharField(max_length = 200, default = 'Professors name')
	rank		= models.IntegerField(default = -1)

	class Meta:
		abstract = True

class University(Entity):
	uni_type 	= models.CharField(max_length = 10, default = 'public')

class Faculty(Entity):
	university 	= models.ForeignKey(University, related_name = 'faculties', on_delete = models.CASCADE, default = 1)

class Department(Entity):
	dep_type 	= models.CharField(max_length=10, default='normal')
	faculty 	= models.ForeignKey(Faculty, related_name = 'departments', on_delete = models.CASCADE, default = 1)

class UserProfile(models.Model):
	user 				= models.OneToOneField(User,related_name = 'profile', on_delete = models.CASCADE)
	department 			= models.ForeignKey(Department, related_name = 'depart_users', on_delete = models.SET_NULL, null = True)
	faculty  			= models.ForeignKey(Faculty, related_name = 'fac_users', on_delete = models.SET_NULL, null = True)
	university 			= models.ForeignKey(University, related_name = 'uni_users', on_delete = models.SET_NULL, null = True)
	level				= models.IntegerField(default = 1)
	gender 				= models.CharField(max_length = 8, default = 'unset')
	count_of_posts 		= models.IntegerField(default = 0)
	count_of_replies 	= models.IntegerField(default = 0)
	academic_stats 		= models.CharField(max_length = 20, default = 'unset')
	last_active_device 	= models.CharField(max_length = 200)
	#topics				= 'relationship with topics'
	#table				= 'relationship with table'
	#posts 				= 'relationship with posts'
	#replies 			= 'relationship with replies'

	@classmethod
	def make_form_new_profile(cls, user_obj, department=None, faculty=None, university=None):
		"""
		Accepts user object and creates his corresponding profile due to his form data. Returns error if existing. 

		>>>make_form_new_profile(user, department)
		<UserProfile object>

		>>>make_form_new_profile()
		Error: expected two paramater
		
		>>>make_form_new_profile(user)
		<UserProfile object> with department = null
		
		>>>make_form_new_profile(existing_user)
		Error: Existing profile
		"""
		user_profile = UserProfile(department=department, faculty=faculty, university=university)
		if not UserProfile.link_profile_to_user(user_obj, user_profile):
			# Existing profile.
			user_profile = user_obj.profile
		user_profile.save()

		return user_profile

	@classmethod
	def link_profile_to_user(cls, user_obj, profile_obj):
		"""(user, profile) -> Boolean

		Accepts User object and profile object and link them together. Returns false if no profile object or error.
		
		>>>link_profile_to_user(user, profile)
		True
		>>>link_profile_to_user(user)
		Error, expected 2 paramaters.
		>>>link_profile_to_user(user, profile=none)
		False
		>>>link_profile_to_user(existing_linked_user, profile)
		False
		"""

		# Missed parameter
		if profile_obj is None:
			return False
		
		user_obj.profile = profile_obj
		user_obj.save()
		return True

	@classmethod
	def make_social_new_profile(backend, user, response, *args, **kwargs):
		"""
		Customize the python_social_auth pipeline flow by saving user profile.
		"""
		first_form_data = request.session.get('first_form_data')
		try:
			department = Department.objects.get(pk = first_form_data['department'])
			faculty 	= Faculty.objects.get(pk = first_form_data['faculty'])
			university = University.objects.get(pk = first_form_data['university'])
		except ObjectDoesNotExist as e:
			raise Http404("An Error encounterd. Please select proper University, Facutly, and Department.")

		UserProfile.objects.create(user=user, department=department, faculty=faculty, university=university)

