from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

username_validator = RegexValidator(r'^\D\s*', 'Name cannot start with digit, should consist of characters.')

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
		widgets = {'password':forms.PasswordInput}
		validators = {'username':username_validator}

	def clean(self):
		"""
		cleaned_data -> ValidationError if possible

		Returns Validation error if and only if:
			- Confirm_password != original_password
		"""
		cleaned_data 		= super(UserSignUpForm, self).clean()
		original_password 	= cleaned_data['password']
		confirm_password 	= cleaned_data['password_confirm']

		if original_password != confirm_password:
			raise forms.ValidationError('The two password are not matched')
		return cleaned_data

	def clean_email(self):
		"""
		cleaned_data['email'] -> email or ValidationError

		Returns Validation error if and only if email already exists with different username.

		"""
		# Using self.cleaned_data as it's already cleaned. and we clean specific attribute. 
		email 			= self.cleaned_data['email']
		# Username can be none due to regex validation.
		username 		= self.cleaned_data['username']
		if email and User.objects.filter(email=email).exclude(username=username).exists():
		    raise forms.ValidationError("Email address must be unique.")
		return email
