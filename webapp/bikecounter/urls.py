from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
#from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import admin
#from rest_framework.urlpatterns import format_suffix_patterns
from api import views

from main.views import *
from account.views import *


urlpatterns = patterns('',
    url(r'^/?$', TemplateView.as_view(template_name='index.html'), name="index"),
    url(r'^login/?$', LoginView.as_view(), name="login"),
    url(r'^logout/?$', LogoutView.as_view(), name="logout"),
    url(r'^register/?$', RegisterView.as_view(), name="register"),
    url(r'^profile/?$', ProfileView.as_view(), name="profile"),
    url(r'^orgs/?$', login_required(OrgListView.as_view()), name="orgs"),
    # Organization selected
    url(r'^(?P<slug>[-\w]+)/home/?$', login_required(OrgHomeView.as_view()), name="org_home"),
    url(r'^(?P<slug>[-\w]+)/schedule/?$', login_required(OrgScheduleView.as_view()), name="org_schedule"),
    url(r'^(?P<slug>[-\w]+)/reports/?$', login_required(ReportHomeView.as_view()), name="reports"),
    url(r'^(?P<slug>[-\w]+)/reports/locations/?$', login_required(ReportLocationsView.as_view()), name="report-locations"),
    url(r'^(?P<slug>[-\w]+)/reports/completion_tracker/?$', login_required(ReportCompletionTrackerView.as_view()), name="report-count-completion-tracker"),
    url(r'^(?P<slug>[-\w]+)/reports/report_export_to_csv/?$', login_required(RequestCSVView.as_view()), name="report_export_to_csv"),

    # new API to generate a CSV within the reports section of the web app
    # I'm trying to copy the pattern used by the buttons 'signup and cancel' written below
    url(r'^(?P<slug>[-\w]+)/reports/report_export_to_csv/generate/?', login_required(GenerateCSV.as_view()), name="generateCSV"),


    url(r'^(?P<slug>[-\w]+)/reports/results_dashboard/?$', login_required(ReportQuickGlanceResultsDashboardView.as_view()), name="results_dashboard"),
    url(r'^(?P<slug>[-\w]+)/signup/(?P<pk>\d+)?$', login_required(ApptSignupView.as_view()), name="appt-signup"),
    url(r'^(?P<slug>[-\w]+)/cancel/(?P<pk>\d+)?$', login_required(ApptCancelView.as_view()), name="appt-cancel"),
    url(r'^(?P<slug>[-\w]+)/detail/(?P<pk>\d+)?$', login_required(cache_page(60)(ApptDetailView.as_view())), name="appt-detail"),
    # API Urls
    #url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/?', 'rest_framework.authtoken.views.obtain_auth_token'),
    #url(r'^api/user/?', views.CurrentUser.as_view(), name='api-user'),
    # TODO - remove /me endpoint after v0.1.8
    url(r'^api/me/?', views.ApptDetail.as_view(), name='api-me'),
    url(r'^api/appts/?', views.ApptDetail.as_view(), name='api-appts'),
    #url(r'^api/orgs/?', views.MeDetail.as_view(), name='api-me'),
    #url(r'^api/org/(?P<pk>\d+)/?', views.LocationViewSet.as_view(), name='api-locations'),
    #url(r'^api/locations/(?P<pk>\d+)?', views.MeDetail.as_view(), name='api-me'),
    url(r'^api/session/(?P<pk>\d+)/start/?', views.ApptViewSet.as_view({'post': 'start'}), name='api-appt-start'),
    url(r'^api/session/(?P<pk>\d+)/end/?', views.ApptViewSet.as_view({'post': 'end'}), name='api-appt-end'),
    url(r'^api/session/(?P<pk>\d+)/reset/?', views.ApptViewSet.as_view({'get': 'reset'}), name='api-appt-reset'),
    url(r'^api/session/(?P<pk>\d+)/survey/?', views.ApptViewSet.as_view({'post': 'survey'}), name='api-post-survey'),
    url(r'^api/session/(?P<pk>\d+)/event/?', views.ApptViewSet.as_view({'post': 'event'}), name='api-post-event'),
    url(r'^admin/', include(admin.site.urls)),
)
