from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.Form):
	user_name 			= forms.CharField(widget = forms.TextInput(attrs={
			'placeholder':'Enter your Name'
		}))
	user_mail			= forms.EmailField(widget = forms.TextInput(attrs={
			'placeholder':'Enter your E-mail'
		}))
	user_password		= forms.CharField(widget = forms.PasswordInput)
		
class UserForm(forms.Form):
	
	class Meta:
		model = User
		