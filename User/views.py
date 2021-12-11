from django.contrib import auth
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .forms import UserRegisterForm, UserLoginForm

# Create your views here.
def user_register(request):
    form = UserRegisterForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        return redirect(f"{reverse('User:login')}?newRegister=1")

    return render(request, 'User/register.html', {'form': form})


def user_login(request):
    form = UserLoginForm(request.POST or None)
    context = {'form': form}
    
    if form.is_valid():
        user = authenticate(
            request,
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        
        if user is not None:
            login(request, user)
            return redirect('User:register')
        
        context['errorCredentials'] = 'Incorrect username or password. Please, try again.'
        
    return render(request, 'User/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('User:login')