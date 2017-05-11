from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.Form):
	user_name	 			= forms.CharField(widget = forms.TextInput(attrs={
			'placeholder':'Enter your Name'
		}))
	user_mail				= forms.EmailField(widget = forms.TextInput(attrs={
			'placeholder':'Enter your E-mail'
		}))
	user_password			= forms.CharField(widget = forms.PasswordInput)
	user_password_confirm	= forms.CharField(widget = forms.PasswordInput)
		
class UserSignUpForm(forms.ModelForm):

	password_confirm 	= forms.CharField(widget = forms.PasswordInput, required = True)
	email 				= forms.EmailField(required = True)
	
	class Meta:
		model 	= User
		fields 	= ['username', 'first_name', 'last_name', 'email', 'password']
		widgets = {'password':forms.PasswordInput}

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
		email 		= self.cleaned_data['email']
		username 	= self.cleaned_data['username']
		if email and User.objects.filter(email=email).exclude(username=username).exists():
		    raise forms.ValidationError("Email address must be unique.")
		return email