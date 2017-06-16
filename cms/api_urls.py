from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from cms import api_views

urlpatterns = [
    url(r'^topics/$', api_views.topics_list, name = 'api_topics_list'),
    url(r'^topics/user$', api_views.user_topics, name = 'api_user_topics'),
    url(r'^topics/(?P<pk>[0-9]+)$', api_views.topic_instance, name = 'api_topic'),
    url(r'^topics/faculty/(?P<fac_id>[0-9]+)$', api_views.topic_faculty, name = 'api_faculty_topics'),
]

urlpatterns = format_suffix_patterns(urlpatterns)