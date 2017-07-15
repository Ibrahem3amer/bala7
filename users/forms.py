from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth import password_validation, hashers
from django.core.exceptions import ValidationError
from users.models import UserProfile

username_validator 		= RegexValidator(r'^[a-zA-Z][a-zA-Z0-9]*[._-]?[a-zA-Z0-9]+$', 'Name cannot start with number, should consist of characters.')

class SignupForm(forms.Form):
	user_name	 			= forms.CharField(
		widget = forms.TextInput(attrs={'placeholder':'Enter your Name'}),
		)
	user_mail				= forms.EmailField(widget = forms.TextInput(attrs={
			'placeholder':'Enter your E-mail'
		}))
	user_password			= forms.CharField(widget = forms.PasswordInput)
	user_password_confirm	= forms.CharField(widget = forms.PasswordInput)
		
class UserSignUpForm(forms.ModelForm):

	username 			= forms.CharField(widget = forms.TextInput, required = True, validators = [username_validator])
	password_confirm 	= forms.CharField(widget = forms.PasswordInput, required = True)
	email 				= forms.EmailField(required = True)
	
	class Meta:
		model 	= User
		fields 	= ['username', 'first_name', 'last_name', 'email', 'password']
		widgets = {'password': forms.PasswordInput}
		validators = {'username':username_validator}

	def clean(self):
		"""
		cleaned_data -> ValidationError if possible

		Returns Validation error if and only if:
			- Confirm_password != original_password
		"""
		cleaned_data = super(UserSignUpForm, self).clean()
		try:
			original_password 	= cleaned_data['password']
			confirm_password 	= cleaned_data['password_confirm']
		except KeyError:
			return cleaned_data

		if original_password != confirm_password:
			raise forms.ValidationError('The two passwords are not matched')
		return cleaned_data

	def clean_password(self):
		"""
		Takes the given password and call django's built-in validators on it. 
		"""
		try:
			password_validation.validate_password(self.cleaned_data['password'])
		except ValidationError as e:
			raise forms.ValidationError(e)
		return self.cleaned_data['password']


	def clean_email(self):
		"""
		cleaned_data['email'] -> email or ValidationError

		Returns Validation error if and only if email already exists with different username.
		"""
		# Using self.cleaned_data as it's already cleaned. and we clean specific attribute. 
		try:
			email 			= self.cleaned_data['email']
			# Username can be none due to regex validation.
			username 		= self.cleaned_data['username']
		except (AttributeError, KeyError): 
			return email

		if email and User.objects.filter(email=email).exclude(username=username).exists():
		    raise forms.ValidationError("Email address must be unique.")
		return email

	def save(self):
		"""
		Creates new user and associate an empty profile to it. 
		"""
		form 				= self.cleaned_data
		usr 				= User.objects.create_user(username = form['username'], email = form['email'], password = form['password'])
		usr.set_password(form['password'])
		usr.save()
		return usr
