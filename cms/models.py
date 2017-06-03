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
