from django.conf.urls import url
from users import views, urls

urlpatterns = [
    url(r'^home', views.home_user, name = 'home_user'),
    url(r'^profile', views.user_profile, name = 'web_user_profile'),
    url(r'^signup/user_details', views.signup_second_form, name = 'web_signup_second_form'),
    url(r'^signup/user_finish', views.signup_second_form, name = 'web_signup_third_form'),
    url(r'^signup', views.display_signup, name = 'web_signup'),
    url(r'^thankyou', views.display_signup, name = 'thankyou'),
]