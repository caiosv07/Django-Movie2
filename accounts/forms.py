from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from .models import User


class Registerform(UserCreationForm):
    email = forms.EmailField
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfilePicForm(forms.ModelForm):
    profile_img = forms.ImageField(label='Profile picture')

    class Meta:
        model = User
        fields = ('profile_img', )