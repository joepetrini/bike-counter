from django.conf import settings
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)
