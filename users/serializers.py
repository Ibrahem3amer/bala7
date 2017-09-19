from rest_framework import serializers
from users.models import *
from cms.models import UserComment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= User
		fields 	= ('id', 'username', 'email', 'password')

class UserProfileSerialzer(serializers.ModelSerializer):
	class Meta:
		model 	= UserProfile
		fields 	= ('university', 'faculty', 'department', 'level', 'gender', 'count_of_posts', 'count_of_replies', 'topics')

class DepratmentSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= Department
		fields 	= ('id', 'name', 'bio', 'headmaster')


class FacultySerializer(serializers.ModelSerializer):

	class Meta:
		model 	= Faculty
		fields 	= ('id', 'name', 'bio', 'headmaster', 'university')


class UniversitySerializer(serializers.ModelSerializer):

	class Meta:
		model 	= University
		fields 	= ('id', 'name', 'bio', 'headmaster')

class DepratmentLinkedSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= Department
		fields 	= ('id', 'name', 'bio', 'headmaster')


class FacultyLinkedSerializer(serializers.ModelSerializer):

	departments = DepratmentLinkedSerializer(many = True)

	class Meta:
		model 	= Faculty
		fields 	= ('id', 'name', 'bio', 'headmaster', 'university', 'departments')


class UniversityLinkedSerializer(serializers.ModelSerializer):

	faculties 	= FacultyLinkedSerializer(many = True)

	class Meta:
		model 	= University
		fields 	= ('name', 'bio', 'headmaster', 'faculties')

class CommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserComment
		fields = ('__all__')

