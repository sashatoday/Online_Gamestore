from django.shortcuts import render, redirect
from gamestore.models import UserProfile, Game
from gamestore.forms import GameForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def show_uploaded_games(request):
    developer = request.user.userprofile.is_developer()
    if not developer:
        return redirect('index')
    games = Game.objects.filter(developer=request.user.userprofile)
    args = {
        'games' : games,
        'developer' : developer,
    }

    return render(request, 'game/uploaded_games.html', args)
    
@login_required(login_url='/login/')
def add_game(request):
    developer = request.user.userprofile.is_developer()
    if not developer:
        return redirect('index')
    form = GameForm()
    args = {
        'form' : form,
        'developer' : developer,
    }
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user.userprofile
            game.save()
            return redirect('uploaded_games') # CHANGE REDIRECTED PAGE LATER!
        else:
            args['form'] = form
            return render(request, 'game/add_game.html', args)
    return render(request, 'game/add_game.html', args)


    
