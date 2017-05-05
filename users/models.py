from django.db import models

# Create your models here.
class Entity(models.Model):
	name 		= models.CharField(max_length=100, default='no name')
	bio 		= models.CharField(max_length=200, default='no data initialized')
	location 	= models.CharField(max_length=200, default='no data initialized')
	headmaster 	= models.CharField(max_length=200, default='Professors name')
	rank		= models.IntegerField(default=-1)

	class Meta:
		abstract = True

class University(Entity):
	uni_type 	= models.CharField(max_length=10, default='public')

class Faculty(Entity):
	university 	= models.ForeignKey(University, related_name = 'faculties', on_delete = models.CASCADE, default = 1)

class Department(Entity):
	dep_type 	= models.CharField(max_length=10, default='normal')
	faculty 	= models.ForeignKey(Faculty, related_name = 'departments', on_delete = models.CASCADE, default = 1)
