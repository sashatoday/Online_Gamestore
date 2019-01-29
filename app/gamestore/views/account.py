from django.shortcuts import render, redirect
from gamestore.models import UserProfile
from gamestore.forms import (
    UserForm, 
    UserUpdateForm, 
    UserProfileUpdateForm,
    ChangePasswordForm,
)
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.db import transaction
from django.contrib.auth.decorators import login_required

def startpage(request):
    if request.user.is_authenticated:
        return render(request, "base.html", {'developer': request.user.userprofile.is_developer()})
    else:
        return render(request, "base.html", {'developer': False})

def login(request):
    next_page = request.GET.get('next') 
    if not next_page: #if request doesn't have ?next= parameter
        next_page = 'index' #keep index page as default redirect
    if request.user.is_authenticated:
        return redirect(next_page)
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
                return redirect(next_page)
        return render(request, "account/login.html", {})

@transaction.atomic
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.clean_password2()
                )
                user.save()
                userProfile = UserProfile(
                    user=user,
                    birthDate=form.cleaned_data['birthDate'],
                    gender=form.cleaned_data['gender']
                )
                userProfile.save()
                auth_login(request, user)
                return redirect('index')
            else:
                return render(request, 'account/signup.html', {'form': form})
        form = UserForm()
        return render(request, 'account/signup.html', {'form': form})

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('index')

@transaction.atomic
@login_required(login_url='/login/')
def profile(request):
    user = request.user
    userprofile = user.userprofile
    username = user.username
    developer = userprofile.is_developer()

    userform = UserUpdateForm(instance=user)
    profileform = UserProfileUpdateForm(instance=userprofile)
    changepasswordform = ChangePasswordForm(user=user)

    args = {
        'userform' : userform,
        'profileform' : profileform,
        'changepasswordform' : changepasswordform,
        'developer' : developer,
    }

    if request.method == 'POST':
        if 'updateprofile' in request.POST:
            userform = UserUpdateForm(request.POST, instance=user)
            profileform = UserProfileUpdateForm(request.POST, instance=userprofile)
            if userform.data['username'] != username:
                userform.add_error('username', "You are not allowed to change your username")
                userform.errors['email'] = ""
                args['userform'] = userform
                return render(request, 'account/profile.html', args)
            if userform.is_valid() and profileform.is_valid():
                userform.save()
                profileform.save()
                return redirect('profile')
            else:
                args['userform'] = userform
                args['profileform'] = profileform
                return render(request, 'account/profile.html', args)
        if 'changepassword' in request.POST:
            changepasswordform = ChangePasswordForm(data=request.POST, user=user)
            if changepasswordform.is_valid():
                changepasswordform.save()
                return redirect('profile')
            else:
                args['changepasswordform'] = changepasswordform
                return render(request, 'account/profile.html', args)

    return render(request, 'account/profile.html', args)
