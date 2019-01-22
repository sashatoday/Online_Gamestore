from django.shortcuts import render, redirect
from gamestore.models import UserProfile
from gamestore.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.db import transaction

def startpage(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user=request.user)
        return render(request, "base.html", {'developer': user.is_developer()})
    else:
        return render(request, "base.html", {'developer': False})

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'account/login.html',
                              {'username': username, 'password': password,
                              'errors': "Your username or password was incorrect."})
            else:
                auth_login(request, user)
                #login success, needs redirect
                return redirect('index')
        return render(request, "account/login.html", {})
    
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        user = User.objects.create_user(
                            first_name=form.clean_first_name(),
                            last_name=form.clean_last_name(),
                            username=form.clean_username(),
                            email=form.clean_email(),
                            password=form.clean_password2()
                        )
                        userProfile = UserProfile(
                            user=user,
                            birthDate=form.clean_birthDate(),
                            age=form.clean_age()
                        )
                except Exception as e:
                    error = "{0}".format(e.message)
                else:
                    user.save()
                    userProfile.save()
                    auth_login(request, user)
                    #signup success, needs redirect
                    return redirect('index')
                return render(request, 'account/signup.html', {'form': form, 'errors': error})
            else:
                return render(request, 'account/signup.html', {'form': form, 'errors': form.errors})
        form = UserForm()
        return render(request, 'account/signup.html', {'form': form, 'errors': ""})

def logout_user(request):
    logout(request)
    return redirect('index')