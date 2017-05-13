from django.db import models
from django.contrib.auth.models import User

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
	department 			= models.ForeignKey(Department, related_name = 'users', on_delete = models.SET_NULL, null = True)
	level				= models.IntegerField(default = 1)
	gender 				= models.CharField(max_length = 8, default = 'unset')
	count_of_posts 		= models.IntegerField()
	count_of_replies 	= models.IntegerField()
	academic_stats 		= models.CharField(max_length = 20, default = 'unset')
	last_active_device 	= models.CharField(max_length = 200)
	#topics				= 'relationship with topics'
	#table				= 'relationship with table'
	#posts 				= 'relationship with posts'
	#replies 			= 'relationship with replies'

	def make_form_new_profile(self, user, department):
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
		

