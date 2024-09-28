from django import forms
from django.contrib.auth.models import User

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)