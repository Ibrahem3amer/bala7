from django.shortcuts import render
from django.http import HttpResponse
from users.models import University, Faculty, Department 


def home_visitor(request):
	return render(request, 'home_visitor.html')

def display_signup(request):
	universities 	= University.objects.all()
	faculties 		= Faculty.objects.all()
	departments		= Department.objects.all()
	return render(request, 'signup.html', {'stage_num': 1, 'universities': universities, 'faculties': faculties, 'departments': departments})
