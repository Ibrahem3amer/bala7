from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from users import api_views

urlpatterns = [
    url(r'^users/$', api_views.users_list),
    url(r'^users/(?P<pk>[0-9]+)$', api_views.user_instance),
    url(r'^universities/$', api_views.universities_list),
    url(r'^universities/linked/(?P<pk>[0-9]+)$', api_views.universities_linked_instance),
    url(r'^universities/(?P<pk>[0-9]+)$', api_views.univerisity_instance),
    url(r'^faculties/$', api_views.faculties_list),
    url(r'^faculties/(?P<pk>[0-9]+)$', api_views.faculty_instance),
]

urlpatterns = format_suffix_patterns(urlpatterns)