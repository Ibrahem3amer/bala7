from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
import unittest
import time

MAX_WAIT = 5

class test_anonymous_visits_website(LiveServerTestCase):
	# Method that waits for page to load explicitly. 
	def wait_for_element_by_id(self, element_id):
		start_time = time.time()
		while True:
			try:
				element = self.browser.find_element_by_id(element_id)
				return element
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)


	# Special method that is started by the beginning of a test runner.	
	def setUp(self):
		self.browser 	= webdriver.Firefox()
		self.signin_url = 'users/signin'
		self.signup_url	= 'users/signup'

	# Special method that is fired by the end of a test runner.
	def tearDown(self):
		self.browser.quit()

	def tesst_home_page_displays_correct_output(self):
		# A user opens website or mobile application.
		home = self.browser
		home.get(self.live_server_url)

		# User sees a landing home contains information about the nature of application, important features.
		# User seese a two buttons to sign-up or to sign-in
		sign_up 	= home.find_element_by_id('id_sign_up')
		sign_in 	= home.find_element_by_id('id_sign_in')

		self.assertIn('Bala7', home.title)
		self.assertEqual(sign_up.get_attribute('href'), home.current_url + self.signup_url)
		self.assertEqual(sign_in.get_attribute('href'), home.current_url + self.signin_url)
	
	def test_user_reach_sign_up(self):
		# User should register his information to be able to use these features.
		self.browser.get(self.live_server_url) 
		
		# Pressing sign up button
		sign_up_btn = self.browser.find_element_by_id('id_sign_up')

		# He’s to be moved to sign up page that contains registration options.
		sign_up_btn.click()

		# Browsing the all available universities and faculties to choose his own. 
		registeration_form 	= self.wait_for_element_by_id('id_registeration_form')
		university_field 	= self.wait_for_element_by_id('id_select_university')
		faculty_field 		= self.wait_for_element_by_id('id_select_faculty')
		department_field 	= self.wait_for_element_by_id('id_select_department')
		self.assertIn(university_field.text, registeration_form.text)
		# He finds a description for each field to the nature of data wanted.
		for input_field in registeration_form.find_elements_by_tag_name('lable'):
			self.assertNotEqual(input_field.get_attribute('for'), '')
		# He searches for his own matching data (university, faculty, department)
		self.assertNotEqual(len(self.browser.find_elements_by_id('id_university_name')), 0)
		self.assertNotEqual(len(self.browser.find_elements_by_id('id_faculty_name')), 0)
		self.assertNotEqual(len(self.browser.find_elements_by_id('id_department_name')), 0)

		# If he can't find his goal, he's register his data to be notified.
		# He finds a form where he can enter his name, email, password and its confirmation.
		notify_form = self.browser.find_element_by_id('id_notify_form')
		future_notification_email = self.browser.find_element_by_id('id_future_notify')
		self.assertIn(future_notification_email, notify_form)

		# He finds 2 buttons to social media auth.
		fb 		= self.browser.find_element_by_id('id_fb_auth')
		twitter = self.browser.find_element_by_id('id_twitter_auth')

		# He finds a side button to sign in with.
		self.assertEqual(self.browser.find_element_by_id('id_signin_side'), self.browser.current_url + self.signin_url)

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

class user_sign_up_using_third_party(LiveServerTestCase):
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