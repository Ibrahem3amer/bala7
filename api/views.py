from django.shortcuts import render
from rest_framework import generics
from api.serializers import UniversitySerializer
from users.models import University

# Create your views here.
class CreateView(generics.ListCreateAPIView):
	queryset 			= University.objects.all()
	serializer_class 	= UniversitySerializer

	def perform_create(self, serializer):
		serializer.save() 