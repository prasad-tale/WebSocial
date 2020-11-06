from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateSignUp
from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

# Create your views here.
from websocial.decorators import unaunthanticated_user

def home(request):
    form = CreateSignUp()

    if request.method == 'POST':
        form = CreateSignUp(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account Successfully Created for ' + user)
            return redirect('/')

    context ={'form':form}
    
    return render(request, 'account/signup.html', context)


def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("userpage/")
        else:
            messages.error(request, "Invalid Credentials")

    context = {}
    
    return render(request, 'account/signup.html', context)


   

def logoutUser(request):

    logout(request)
    return redirect('/')
