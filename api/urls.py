from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import CreateView

urlpatterns = {
    url(r'^createuniversity/$', CreateView.as_view(), name="create"),
}

urlpatterns = format_suffix_patterns(urlpatterns)