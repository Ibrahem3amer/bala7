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
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from users import views

admin.site.site_header = 'Najiba Admins'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_visitor, name = 'home_visitor'),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^api/', include('users.api_urls')),
    url(r'^topics/', include('cms.urls')),
    url(r'^api/', include('cms.api_urls')),
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^api_docs/', include_docs_urls(title='Najiba APIs'))
]


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

