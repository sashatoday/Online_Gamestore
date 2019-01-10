from django.shortcuts import render
from gamestore.models import UserProfile
from gamestore.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate

def startpage(request):
    return render(request, "base.html", {})

def login(request):
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
            return render(request, 'start_page.html', {'username': user.username})
    return render(request, "account/login.html", {})
    
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.clean_username(),
                email=form.clean_email(),
                password=form.clean_password2()
            )
            user.save()
            userProfile = UserProfile(
                user=user,
                birthDate=form.clean_birthDate()
            )
            userProfile.save()
            auth_login(request, user)
            return render(request, 'start_page.html', {'username': userProfile.user.username})
        else:
            return render(request, 'account/signup.html', {'form': form, 'errors': form.errors})
    form = UserForm()
    return render(request, 'account/signup.html', {'form': form, 'errors': ""})