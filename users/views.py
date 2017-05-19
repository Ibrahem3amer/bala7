from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users.models import University, Faculty, Department, UserProfile 
from users.forms import UserSignUpForm


def home_visitor(request):
	if request.user.is_authenticated:
		return home_user(request)
	return render(request, 'home_visitor.html')

@login_required
def home_user(request):
	user = request.user
	profile_error = ''
	try:
		user_profile = user.profile
	except AttributeError:
		new_profile = UserProfile()
		new_profile.user = user
		new_profile.save()
		profile_error = 'Please complete your profile.'
	return render(request, 'home_user.html', {'profile_error': profile_error})

@login_required
def user_profile(request):
	return render(request, 'profile/profile.html')	

def display_signup(request):
	universities 	= University.objects.all()
	faculties 		= Faculty.objects.all()
	departments		= Department.objects.all()
	return render(request, 'registration/signup.html', {'stage_num': 1, 'universities': universities, 'faculties': faculties, 'departments': departments})

def signup_second_form(request):
	first_form_data = {}
	if request.method == 'POST': 
		first_form_data = request.session.get('first_form_data')
		signup_form 	= UserSignUpForm(request.POST)
		if signup_form.is_valid():
			user 			= signup_form.save()
			form_department = get_object_or_404(Department, pk = first_form_data['department'])
			form_faculty 	= get_object_or_404(Faculty, pk = first_form_data['faculty'])
			form_university = get_object_or_404(University, pk = first_form_data['university'])
			user_profile 	= UserProfile.make_form_new_profile(user, form_department, form_faculty, form_university)
			return redirect('home_user')
	else:
		university 	= request.GET.get('selected_university', None)
		faculty 	= request.GET.get('selected_faculty', None)
		department 	= request.GET.get('selected_department', None)

		# Redirect user to first form with error of he didn't entered data.
		if university is None or faculty is None or department is None:
			return redirect('web_signup')
		first_form_data 					= {'university':university, 'faculty':faculty, 'department':department}
		request.session['first_form_data'] 	= first_form_data
		signup_form 						= UserSignUpForm()

	return render(request, 'registration/signup_second_form.html', {'stage_num':2, 'form': signup_form})

def signup_third_form(request):
	return ('third_form')