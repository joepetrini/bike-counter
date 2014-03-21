from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from rest_framework import viewsets, routers


from main.views import *
from account.views import *

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = User

class GroupViewSet(viewsets.ModelViewSet):
    model = Group

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = patterns('',
    url(r'^/?$', TemplateView.as_view(template_name='index.html'), name="index"),
    url(r'^login/?$', LoginView.as_view(), name="login"),
    url(r'^logout/?$', LogoutView.as_view(), name="logout"),
    url(r'^profile/?$', ProfileView.as_view(), name="profile"),
    url(r'^orgs/?$', login_required(OrgListView.as_view()), name="orgs"),
    url(r'^(?P<slug>[-\w]+)/home/?$', login_required(OrgHomeView.as_view()), name="org_home"),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
