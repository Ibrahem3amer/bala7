from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
import unittest
import time

class test_anonymous_visits_website(LiveServerTestCase):
	#special method that is started by the beginning of a test runner.	
	def setUp(self):
		self.browser = webdriver.Firefox()

	#special method that is fired by the end of a test runner.
	def tearDown(self):
		self.browser.quit()

	def home_page_displays_correct_output(self):
		# A user opens website or mobile application.
		self.browser.get(self.live_server_url)

		# User sees a landing home contains information about the nature of application, important features.
		self.assertIn('Bala7', self.browser.title)
	
	# User should register his information to be able to use these features. 
		# Pressing sign up button
			# He’s to be moved to sign up page that contains registration options.
			# Browsing the all available universities and faculties to choose his own. 
				# If he can't find his goal, he's register his data to be notified.
			# He finds a form where he can enter his name, email, password and its confirmation.
				# He finds 2 buttons to social media auth.
				# He finds a description for each field to the nature of data wanted.
			# He finds a side button to sign in with.

class user_sign_up_using_form(LiveServerTestCase):
	#special method that is started by the beginning of a test runner.	
	def setUp(self):
		self.browser = webdriver.Firefox()

	#special method that is fired by the end of a test runner.
	def tearDown(self):
		self.browser.quit()

	# System verifies name validity, E-mail uniqueness, and password matching.
				# System raises an error with details if any found. 
	# System validates the incoming data and then signing in the user and moves him back to home page.
	# More on that later. 

class test_user_sign_up_using_third_party(LiveServerTestCase):
	#special method that is started by the beginning of a test runner.	
	def setUp(self):
		self.browser = webdriver.Firefox()

	#special method that is fired by the end of a test runner.
	def tearDown(self):
		self.browser.quit()

	# System verifies name validity, E-mail uniqueness, and password matching.
				# System raises an error with details if any found. 
	# System validates the incoming data and then signing in the user and moves him back to home page.
	# More on that later. 

class user_sign_in_using_form(LiveServerTestCase):
	#special method that is started by the beginning of a test runner.	
	def setUp(self):
		self.browser = webdriver.Firefox()

	#special method that is fired by the end of a test runner.
	def tearDown(self):
		self.browser.quit()

	# User should sign in if he’s already a member.
		# User should press the sign-in button to be able to enter his data.
		# User’s to be asked to choose either direct login (email and password) or social media login.
	# In case of direct login: system accepts user’s email and password.
	# System validates incoming data against any suspicious input. 
	# System authorize given input.
	# System returns error message in case of not found users.
	# System returns success message with current user logged-in. 

class user_sign_in_using_third_party(LiveServerTestCase):
	#special method that is started by the beginning of a test runner.	
	def setUp(self):
		self.browser = webdriver.Firefox()

	#special method that is fired by the end of a test runner.
	def tearDown(self):
		self.browser.quit()

	# User should sign in if he’s already a member.
		# User should press the sign-in button to be able to enter his data.
		# User’s to be asked to choose either direct login (email and password) or social media login.
	# In case of social media login: 
	# System connects to facebook/twitter to verify user’s email.
	# System returns to validate the existence of user in current users’ base. 

if __name__ == '__main__':
	unittest.main()