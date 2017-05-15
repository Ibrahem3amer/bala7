from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from users.models import University, Faculty, Department, UserProfile 
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
	first_form_data = {}
	if request.method == 'POST': 
		first_form_data = request.session.get('first_form_data')
		signup_form = UserSignUpForm(request.POST)
		if signup_form.is_valid():
			user 				= signup_form.save(commit=True)
			# In case that request has some problems with session object, return pk = 1.
			form_department 	= get_object_or_404(Department, pk = max(first_form_data['department'], 1))
			form_faculty 		= get_object_or_404(Faculty, pk = max(first_form_data['faculty'], 1))
			form_university 	= get_object_or_404(University, pk = max(first_form_data['university'], 1))
			user_profile 		= UserProfile.make_form_new_profile(user)
			return redirect('home_user')
	else:
		university 							= request.GET.get('selected_university', None)
		faculty 							= request.GET.get('selected_faculty', None)
		department 							= request.GET.get('selected_department', None)

		# Redirect user to first form with error of he didn't entered data.
		if university is None or faculty is None or department is None:
			return redirect('web_signup')
		first_form_data 					= {'university':university, 'faculty':faculty, 'department':department}
		request.session['first_form_data'] 	= first_form_data
		signup_form 						= UserSignUpForm()

	return render(request, 'signup_second_form.html', {'stage_num':2, 'form': signup_form})

def signup_third_form(request):
	return ('third_form')