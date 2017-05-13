from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import University, Faculty, Department 
from users.forms import UserSignUpForm


def home_visitor(request):
	return render(request, 'home_visitor.html')

def home_user(request):
	return render(request, 'home_visitor.html')

def display_signup(request):
	universities 	= University.objects.all()
	faculties 		= Faculty.objects.all()
	departments		= Department.objects.all()
	return render(request, 'signup.html', {'stage_num': 1, 'universities': universities, 'faculties': faculties, 'departments': departments})

def signup_second_form(request):
	if request.method == 'POST':
		# Todo: passing university and faculty details to user instance. 
		signup_form = UserSignUpForm(request.POST)
		if signup_form.is_valid():
			signup_form.save(commit=True)
			return redirect('home_user')
	else:
		# Todo: accept university and faculty detials.
		signup_form = UserSignUpForm()

	return render(request, 'signup_second_form.html', {'stage_num':2, 'form': signup_form})

def signup_third_form(request):
	return ('third_form')