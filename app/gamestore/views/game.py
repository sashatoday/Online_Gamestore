from django.shortcuts import render, redirect
from gamestore.models import UserProfile
from gamestore.forms import GameForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def show_uploaded_games(request):
    user = UserProfile.objects.get(user=request.user)
    # UNCOMMENT LATER!
    #if not user.is_developer():
    #    return redirect('index')

    return render(request, 'game/uploaded_games.html', {})
    
@login_required(login_url='/login/')
def add_game(request):
    user = UserProfile.objects.get(user=request.user)
    # UNCOMMENT LATER!
    #if not user.is_developer():
    #    return redirect('index')
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = user
            game.save()
            #adding success, needs redirect
            return redirect('index') # CHANGE REDIRECTED PAGE LATER!
        else:
            return render(request, 'game/add_game.html', {'form': form, 'errors': form.errors})
    form = GameForm()
    return render(request, 'game/add_game.html', {'form': form, 'errors': ""})