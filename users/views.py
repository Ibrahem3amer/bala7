from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from users.models import University, Faculty, Department, UserProfile 
from users.forms import UserSignUpForm
from cms.models import UserTopics, Task, Material, UserContribution, Event

UPDATES_LIMIT = 3

def home_visitor(request):
	if request.user.is_authenticated:
		return home_user(request)
	return render(request, 'home_visitor.html')

@login_required
def home_user(request):
	"""
	Displays logged-in user homepage, creates default profile in case of not. 
	"""
	user = request.user
	profile_error = ''
	try:
		user_profile = user.profile
	except AttributeError:
		# Create default profile. 
		new_profile = UserProfile()
		new_profile.user 	= user
		new_profile.topics 	= None 
		new_profile.save()
		messages.add_message(request, messages.INFO, 'Please complete your profile')

	# Getting user tasks deadlines. 
	tasks = Task.get_closest_tasks(request)

	# Getting local/global evetns and app updates.
	events = Event.get_closest_events(request)

	# Getting user materials updateds.
	primary_materials = Material.get_user_materails(user_obj=request.user, limit=UPDATES_LIMIT)
	secondary_materials = UserContribution.get_user_materails(user_obj=request.user, limit=UPDATES_LIMIT)

	return render(
		request,
		'home_user.html',
		{
			'tasks': tasks,
			'primary': primary_materials,
			'secondary': secondary_materials, 
			'events': events
		}
	)

@login_required
def user_profile(request):
	"""
	Gathers user's availabe topics, displays user profile page.
	"""

	# Assign a default profile to user if profile doesn't exist.
	try:
		avaliable_topics = UserTopics.get_topics_choices(request.user)
		user_topics_ids = [topic.id for topic in request.user.profile.topics.all()]
	except UserProfile.DoesNotExist:
		return home_user(request)
	return render(request, 'profile/profile.html', {'avaliable_topics': avaliable_topics, 'user_topics_ids': user_topics_ids})

@login_required
def update_user_username(request):
		"""
		Takes a post request and validates new username to change it.
	
		>>>update_user_username(request_that_has_correct_username)
		Success, redirection to profile page. 
		>>>update_user_username(request_that_has_non_authenticated_user)
		Redirection to login page
		>>>update_user_username(request_that_has_invalid_username)
		Error message, redirection to profile page.

		"""	
		if request.method == 'POST':				

			if UserProfile.validate_name(request.POST['new_username']):
				UserProfile.change_username(request.POST['new_username'], request.user)
				messages.add_message(request, messages.SUCCESS, 'Username successfully changed')
				return user_profile(request)
			else:
				msg = 'Username is not valid or already exists. Try another one.'
				messages.add_message(request, messages.ERROR, msg)
				return render(request, 'profile/profile.html')
		else:
			return redirect('home_user')

@login_required
def update_user_email(request):
		"""
		Takes a post request and validates new email to change it.

		"""
		if not request.POST['new_usermail']:
			msg = 'Email cannot be empty.'
			messages.add_message(request, messages.ERROR, msg)
			return render(request, 'profile/profile.html')
		if UserProfile.validate_mail(request.POST['new_usermail'], request.POST['new_usermail_confirmation']):
			UserProfile.change_mail(request.POST['new_usermail'], request.user)
			msg = 'Email successfully changed.'
			messages.add_message(request, messages.SUCCESS, msg)
			return render(request, 'profile/profile.html')
		else:
			msg = 'Email is not valid or does not match.'
			messages.add_message(request, messages.ERROR, msg)
			return render(request, 'profile/profile.html')
		
		return redirect('home_user')

@login_required
def update_user_password(request):
		"""
		Takes a post request and validates password to change it.
		"""
		# Check for emptiness
		if not request.POST['old_password'] or not request.POST['new_password'] or not request.POST['new_password_confirm']:
			msg = 'password fields cannot be empty.'
			messages.add_message(request, messages.ERROR, msg)
			return render(request, 'profile/profile.html')

		# Check if password is valid
		if UserProfile.validate_new_password(request.POST['old_password'], request.POST['new_password'], request.POST['new_password_confirm'], request.user):
			UserProfile.change_password(request.POST['new_password'], request.user)
			msg = 'Password successfully changed.'
			messages.add_message(request, messages.SUCCESS, msg)
			return render(request, 'profile/profile.html')
		else:
			msg = 'Password is not valid. It must be at least 8 characters length, mix of letters and numbers.'
			messages.add_message(request, messages.ERROR, msg)
			return render(request, 'profile/profile.html')
		
		return redirect('home_user')

@login_required
def update_user_education_info(request):
	"""
	Takes post request that contains updated info to be replaced with the old one.
	"""
	if request.method == 'POST':
		new_info = {}
		try:
			new_info['new_university_id'] 	= request.POST['universities-hidden']
			new_info['new_faculty_id'] 		= request.POST['faculties-hidden']
			new_info['new_department_id'] 	= request.POST['departments-hidden']
			new_info['new_section_number'] 	= request.POST['new_section_number']
		except AttributeError:
			msg = 'University, faculty and department cannot be empty.'
			messages.add_message(request, messages.ERROR, msg)
			return render(request, 'profile/profile.html')

		if UserProfile.update_education_info(new_info, request.user):
			msg = 'Your educational info updated successfully.'
			messages.add_message(request, messages.SUCCESS, msg)
			return render(request, 'profile/profile.html')
		else:
			msg = 'Invalid educational info. Try again.'
			messages.add_message(request, messages.ERROR, msg)
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
			msg = 'Please select your university, faculty, and department.'
			messages.add_message(request, messages.ERROR, msg)
			return redirect('web_signup')
		first_form_data 					= {'university':university, 'faculty':faculty, 'department':department}
		request.session['first_form_data'] 	= first_form_data
		signup_form 						= UserSignUpForm()

	return render(request, 'registration/signup_second_form.html', {'stage_num':2, 'form': signup_form})

def signup_third_form(request):
	return ('third_form')