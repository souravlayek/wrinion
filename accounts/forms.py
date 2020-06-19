from django import forms
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profilepic', 'interest']
