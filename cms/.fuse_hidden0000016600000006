from django.conf.urls import url
from cms import views

urlpatterns = [
    url(r'^(?P<dep_id>[0-9]+)/(?P<topic_id>[0-9]+)$', views.get_topic, name = 'get_topic'),
    url(r'^update_topics$', views.update_user_topics, name = 'update_user_topics'),
    url(r'^materials/add$', views.add_material, name = 'add_material_web'),
    url(r'^doctors/(?P<doctor_id>[0-9]+)$', views.doctor_main_page, name = 'display_doctor'),
    url(r'^table/main/results$', views.query_table, name = 'web_query_table'),
    url(r'^table/main$', views.dep_table_main, name = 'web_dep_table'),
    url(r'^table/available_table$', views.available_table, name = 'web_available_table'),
    
]