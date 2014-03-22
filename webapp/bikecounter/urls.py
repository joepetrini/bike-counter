from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import admin
#from rest_framework import viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

from main.views import *
from account.views import *

# Routers provide an easy way of automatically determining the URL conf.
#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
#router.register(r'me', views.MeDetail.as_view())

urlpatterns = patterns('',
    url(r'^/?$', TemplateView.as_view(template_name='index.html'), name="index"),
    url(r'^login/?$', LoginView.as_view(), name="login"),
    url(r'^logout/?$', LogoutView.as_view(), name="logout"),
    url(r'^profile/?$', ProfileView.as_view(), name="profile"),
    url(r'^orgs/?$', login_required(OrgListView.as_view()), name="orgs"),
    url(r'^(?P<slug>[-\w]+)/home/?$', login_required(OrgHomeView.as_view()), name="org_home"),
    url(r'^(?P<slug>[-\w]+)/schedule/?$', login_required(OrgScheduleView.as_view()), name="org_schedule"),
    #url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/?', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api/me/?', views.MeDetail.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
