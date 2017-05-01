from django.db import models

# Create your models here.
class Entity(models.Model):
	class Meta:
		abstract = True
	
	name 		= models.CharField(max_length=100, default='no name')
	bio 		= models.CharField(max_length=200, default='no data initialized')
	location 	= models.CharField(max_length=200, default='no data initialized')
	headmaster 	= models.CharField(max_length=200, default='Professors name')
	rank		= models.IntegerField(default=-1)

class University(Entity):
	uni_type 	= models.CharField(max_length=10, default='public')

class Faculty(Entity):
	pass

class Department(Entity):
	dep_type 	= models.CharField(max_length=10, default='normal')
