from django.conf import settings
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from .models import Organization, Appointment

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)


class OrgListView(ListView):
    model = Organization
    template_name = 'select_org.html'

    #def get_queryset(self):
    #    pass


class OrgHomeView(DetailView):
    model = Organization
    template_name = 'org_home.html'

    def get_context_data(self, **kwargs):
        context = super(OrgHomeView, self).get_context_data(**kwargs)
        sessions = Appointment.objects.filter(user=self.request.user, organization=self.object)
        context['sessions'] = sessions
        return context