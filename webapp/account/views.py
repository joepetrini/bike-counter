from django.conf import settings
from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login, logout, authenticate
#from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView, View, CreateView
from .forms import ProfileForm, UserForm


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        #return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = UserForm
    template_name = 'register.html'
    success_url = settings.LOGIN_REDIRECT_URL  #'/orgs'

    def form_valid(self, form):
        resp = super(RegisterView, self).form_valid(form)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        auth_login(self.request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)


class ProfileView(FormView):
    form_class = ProfileForm
    template_name = 'profile.html'
