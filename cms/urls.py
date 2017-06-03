from django.conf.urls import url
from cms import views, urls

urlpatterns = [
    url(r'^(?P<dep_id>[0-9]+)/(?P<topic_id>[0-9]+)', views.get_topic, name = 'get_topic'),
]