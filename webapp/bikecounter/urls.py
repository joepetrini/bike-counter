from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User, Group
from django.views.generic import TemplateView
from rest_framework import viewsets, routers

from django.contrib import admin
admin.autodiscover()

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
    # Examples:
    url(r'^/?$', TemplateView.as_view(template_name='index.html'), name="index"),
    # url(r'^$', 'bikecounter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
