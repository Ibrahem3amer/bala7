from django import forms

class SignupForm(forms.Form):
	user_name 			= forms.CharFeild()
	user_mail			= forms.EmailField()
		