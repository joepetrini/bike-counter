from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserForm(UserCreationForm):
    #password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    """
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        login(self.request, user)
        return user
    """
     # june 2016, forcing usernames to be all lower case before being saved
    def clean(self):
        # Then call the clean() method of the super  class

        cleaned_data = super(UserForm, self).clean()
         # ... do some cross-fields validation for the subclass

        cleaned_data['username'] = self.cleaned_data.get('username', None)

         # Finally, return the cleaned_data
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['twitter']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        #self.fields
