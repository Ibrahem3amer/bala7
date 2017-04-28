from django.shortcuts import render
from django.http import HttpResponse


def home_visitor(request):
	return render(request, 'home_visitor.html')

def display_signup(request):
	return render(request, 'signup.html', {'stage_num': 1})
