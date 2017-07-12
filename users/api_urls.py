from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from users import api_views
from cms import api_views as cms_views

urlpatterns = [
    url(r'^users/$', api_views.users_list, name = 'api_users_list'),
    url(r'^users/tasks$', cms_views.tasks_list, name = 'api_user_tasks'),
    url(r'^users/(?P<pk>[0-9]+)$', api_views.user_instance, name = 'api_user'),
    url(r'^universities/$', api_views.universities_list, name = 'api_univs_list'),
    url(r'^universities/(?P<pk>[0-9]+)$', api_views.univerisity_instance, name = 'api_univ'),
    url(r'^universities/linked/(?P<pk>[0-9]+)$', api_views.universities_linked_instance, name = 'api_univ_link'),
    url(r'^faculties/$', api_views.faculties_list, name = 'api_facs_list'),
    url(r'^faculties/university/(?P<uni_pk>[0-9]+)$', api_views.faculties_university_list, name = 'api_fac_univ'),
    url(r'^faculties/(?P<pk>[0-9]+)$', api_views.faculty_instance, name = 'api_fac'),
    url(r'^departments/$', api_views.departments_list, name = 'api_deps_list'),
    url(r'^departments/faculty/(?P<fac_pk>[0-9]+)$', api_views.departments_faculty_list, name = 'api_dep_fac'),
    url(r'^departments/(?P<pk>[0-9]+)$', api_views.departments_instance, name = 'api_dep'),
]

urlpatterns = format_suffix_patterns(urlpatterns)