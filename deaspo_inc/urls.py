"""deaspo_inc URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import staticfiles
from django.contrib import admin
from deaspo import views
from deaspo.forms import RegistrationFormWithNext
import services

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^services/?$', views.services, name='services'),
    url(r'^service/(\d+)/?$', views.service, name='service'),
    url(r'^projects/?$',views.projects,name='projects'),
    url(r'^project/(\d+)/?$', views.project,name='project'),
    url(r'^service/(\d+)/(\d+)/order$', views.order, name='order'),
    url(r'check/(\d+)/(\d+)/?$', views.selfCheck,name='check'),
    url(r'login/?$', views.signin,name='login'),
    url(r'logout/?$',views.sign_out,name='logout'),
    url(r'profile/?$', views.profile,name='profile'),
    url(r'register/?$',views.RegisterView.as_view(),name='register'),
    url(r'update_profile/(\d+)/?$',views.update_profile,name='update_profile'),
    url(r'delete_user/(\d+)/?$',views.del_user,name='delete_user'),
    url(r'about/?$',views.about,name="about"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
#    url(r'^test/?$',views.testing,name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

