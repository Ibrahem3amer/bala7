from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from cms import api_views
from users.api_views import main_table, user_table

urlpatterns = [
    url(r'^topics/$', api_views.topics_list, name = 'api_topics_list'),
    url(r'^topics/user$', api_views.user_topics, name = 'api_user_topics'),
    url(r'^topics/(?P<topic_id>[0-9]+)/materials/$', api_views.materials_list, name = 'api_materials_list'),
    url(r'^topics/(?P<pk>[0-9]+)$', api_views.topic_instance, name = 'api_topic'),
    url(r'^topics/faculty/(?P<fac_id>[0-9]+)$', api_views.topic_faculty, name = 'api_faculty_topics'),
    url(r'^topics/query_table/$', api_views.query_dep_table, name = 'api_query_table'),
    url(r'^users/(?P<user_id>[0-9]+)/main_table/$', main_table, name = 'api_main_table'),
    url(r'^users/(?P<user_id>[0-9]+)/table/$', user_table, name = 'api_user_table'),
]

urlpatterns = format_suffix_patterns(urlpatterns)