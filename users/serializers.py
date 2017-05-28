from rest_framework import serializers
from users.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= User
		fields 	= ('id', 'username', 'email', 'password')


class DepratmentSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= Department
		fields 	= ('id', 'name', 'bio', 'headmaster', 'dep_type')


class FacultySerializer(serializers.ModelSerializer):

	class Meta:
		model 	= Faculty
		fields 	= ('id', 'name', 'bio', 'headmaster', 'university')


class UniversitySerializer(serializers.ModelSerializer):

	class Meta:
		model 	= University
		fields 	= ('id', 'name', 'bio', 'headmaster', 'uni_type')

class DepratmentLinkedSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= Department
		fields 	= ('id', 'name', 'bio', 'headmaster', 'dep_type')


class FacultyLinkedSerializer(serializers.ModelSerializer):

	departments = DepratmentLinkedSerializer(many = True)

	class Meta:
		model 	= Faculty
		fields 	= ('id', 'name', 'bio', 'headmaster', 'university', 'departments')


class UniversityLinkedSerializer(serializers.ModelSerializer):

	faculties 	= FacultyLinkedSerializer(many = True)

	class Meta:
		model 	= University
		fields 	= ('name', 'bio', 'headmaster', 'uni_type', 'faculties')

