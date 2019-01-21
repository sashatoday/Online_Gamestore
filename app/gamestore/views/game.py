from django.shortcuts import render, redirect
from gamestore.models import UserProfile
from gamestore.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def show_uploaded_games(request):

    return render(request, 'game/uploaded_games.html', {})
    
@login_required(login_url='/login/')
def add_game(request):

    return render(request, 'game/add_game.html', {})