"""bala7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_visitor, name = 'home_visitor'),
    url(r'^users/home', views.home_user, name = 'home_user'),
    url(r'^users/signin', views.display_signup, name = 'web_signin'),
    url(r'^users/signup/user_details', views.signup_second_form, name = 'web_signup_second_form'),
    url(r'^users/signup/user_finish', views.signup_second_form, name = 'web_signup_third_form'),
    url(r'^users/signup', views.display_signup, name = 'web_signup'),
    url(r'^users/thankyou', views.display_signup, name = 'thankyou'),
    url('', include('social_django.urls', namespace='social')),
]
