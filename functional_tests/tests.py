from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class anonymous_visits_website(unittest.TestCase):
	#A user opens website or mobile application.
	#User sees a landing home contains information about the nature of application, important features.
	#User should register his information to be able to use these features. 
	#2 ways of registration are available:
		#Pressing sign up button
			#He’s to be moved to sign up page that contains registration options.
		#Browsing the all available universities and faculties to choose his own. 
			#system connects to user’s facebook/twitter profile to gather basic information (name, email, phone, age)
			#He’s to be moved to sign up page with his choice data to populate the matching fields of registration form.
