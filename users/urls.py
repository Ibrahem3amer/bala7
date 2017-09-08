from django.conf.urls import url
from users import views
from cms.views import user_table

urlpatterns = [
    url(r'^home', views.home_user, name = 'home_user'),
    url(r'^profile/change_username', views.update_user_username, name = 'web_change_username'),
    url(r'^profile/change_email', views.update_user_email, name = 'web_change_email'),
    url(r'^profile/change_password', views.update_user_password, name = 'web_change_password'),
    url(r'^profile/change_info', views.update_user_education_info, name = 'web_change_info'),
    url(r'^profile/table', user_table, name = 'web_user_table'),
    url(r'^profile', views.user_profile, name = 'web_user_profile'),
    url(r'^signup/user_details', views.signup_second_form, name = 'web_signup_second_form'),
    url(r'^signup/user_finish', views.signup_second_form, name = 'web_signup_third_form'),
    url(r'^signup', views.display_signup, name = 'web_signup'),
    url(r'^thankyou', views.display_signup, name = 'thankyou'),
]