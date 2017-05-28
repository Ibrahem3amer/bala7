from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.serializers import *
from users.models import *
from django.contrib.auth.models import User

@api_view(['GET', 'POST'])
def users_list(request, format = None):
	"""
	Return a list of users if GET, creates a new one if POST
	"""
	if request.method == 'GET':
		users 				= User.objects.all()
		users_serialized 	= UserSerializer(users, many = True)
		return Response(users_serialized.data)
	elif request.method == 'POST':
		new_instance = UserSerializer(data = request.data)
		if new_instance.is_valid():
			new_instance.save()
			return Response(new_instance.data, status = status.HTTP_201_CREATED)
		return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_instance(request, pk, format = None):
	"""
	Returns a user instance if GET, updates/deletes one due to pk if PUT or DELETE
	"""
	try:
		user_instance = User.objects.get(pk = pk)
	except User.DoesNotExist:
		return Response(status = status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		user_serialized = UserSerializer(user_instance)
		return Response(user_serialized.data)

	elif request.method == 'PUT':
		user_serialized = UserSerializer(user_instance, data = request.data)
		if user_serialized.is_valid():
			user_serialized.save()
			return Response(user_serialized.data)
		return Response(user_serialized.errors, status = status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		user_instance.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def universities_list(request, format = None):
	"""
	Returns a list of universities if GET, 400-bad-request otherwise.
	"""
	if request.method == 'GET':
		universities 		= University.objects.all()
		univrs_serialized 	= UniversitySerializer(universities, many = True)
		return Response(univrs_serialized.data)
	else:
		return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def universities_linked_instance(request, pk, format = None):
	"""
	Returns a university instance with its linked faculties and departments if GET, 400-bad-request otherwise.
	"""
	try:
		university_obj = University.objects.get(pk = pk)
	except University.DoesNotExist:
		return Response(status = status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		university_serialized = UniversityLinkedSerializer(university_obj)
		return Response(university_serialized.data)


@api_view(['GET'])
def univerisity_instance(request, pk, format = None):
	"""
	Returns a university instance if GET, 400-bad-request otherwise.
	"""
	try:
		university_obj = University.objects.get(pk = pk)
	except University.DoesNotExist:
		return Response(status = status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		university_serialized = UniversitySerializer(university_obj)
		return Response(university_serialized.data)

@api_view(['GET'])
def faculties_list(request, format = None):
	"""
	Returns a list of faculties if GET, 400-bad-request otherwise.
	"""
	if request.method == 'GET':
		faculties 				= Faculty.objects.all()
		faculties_serialized 	= FacultySerializer(faculties, many = True)
		return Response(faculties_serialized.data)
	else:
		return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def faculty_instance(request, pk, format = None):
	"""
	Returns a faculty instance if GET, 400-bad-request otherwise.
	"""
	try:
		faculty_obj = Faculty.objects.get(pk = pk)
	except Faculty.DoesNotExist:
		return Response(status = status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		faculties_serialized = FacultySerializer(faculty_obj)
		return Response(faculties_serialized.data)