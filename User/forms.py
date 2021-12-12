from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        max_length=50,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'form3Example4c'
        }),
    )
    password2 = forms.CharField(
        label='Password confirmation',
        max_length=50,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'form3Example4cd'    
        }),
    )
    class Meta:
        model = User
        fields = ('username',)
        labels = {
            'username': 'Username'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'form3Example1c'
            })
        }
        
          
class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'form3Example1c'
        }),
    )
    password = forms.CharField(
        label='Password',
        max_length=50, 
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'form3Example4c'    
        }),
    )
    