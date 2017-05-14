from django.shortcuts import render, redirect
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
	if request.method == 'POST':
		# Todo: passing university and faculty details to user instance. 
		signup_form = UserSignUpForm(request.POST)
		if signup_form.is_valid():
			user = signup_form.save(commit=False)
			# Todo: pass university and faculty as ids and not names. 
			form_department = Department.objects.get(id = request.POST['department'])
			user_profile = UserProfile.make_new_profile(user)
			return redirect('home_user')
	else:
		# Todo: accept university and faculty detials.
		university 		= request.GET['selected_university']
		faculty 		= request.GET['selected_faculty']
		department 		= request.GET['selected_department']
		first_form_data = {'university':university, 'faculty':faculty, 'department':department}
		signup_form 	= UserSignUpForm()

	return render(request, 'signup_second_form.html', {'stage_num':2, 'form': signup_form, 'first_form':first_form_data})

def signup_third_form(request):
	return ('third_form')