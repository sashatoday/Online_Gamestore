from django.shortcuts import render, redirect
from gamestore.models import *
from gamestore.forms import GameForm, GameUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required(login_url='/login/')
def search_game(request):
    developer = request.user.userprofile.is_developer()
    # TODO: process search input and filter objects
    games = Game.objects.all()
    args = {
        'games' : games,
        'developer' : developer,
    }
    return render(request, "game/search_game.html", args)

@login_required(login_url='/login/')
def show_my_games(request):
    user = request.user.userprofile
    developer = user.is_developer()
    purchased_games = Game.objects.filter(purchasedGame__in=Purchase.objects.filter(buyer=user))
    games = Game.objects.all()
    args = {
        'games' : purchased_games,
        'developer' : developer,
    }
    return render(request, "game/my_games.html", args)

@login_required(login_url='/login/')
def game_description(request, game_id):
    user = request.user.userprofile
    developer = user.is_developer()
    game = get_object_or_404(Game, id=game_id)
    owner = False
    if game.developer == request.user.userprofile:
        owner = True

    purchased_games = Game.objects.filter(purchasedGame__in=Purchase.objects.filter(buyer=user))
    if game in purchased_games:
        purchased_game = True
    else:
        purchased_game = False

    args = {
        'game' : game,
        'developer' : developer,
        'owner' : owner,
        'purchased_game' : purchased_game,
    }
    return render(request, "game/game_description.html", args)

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
            return redirect('uploaded_games')
        else:
            args['form'] = form
            return render(request, 'game/add_game.html', args)
    return render(request, 'game/add_game.html', args)

@login_required(login_url='/login/')
def edit_game(request, game_id):
    developer = request.user.userprofile.is_developer()
    if not developer:
        return redirect('index')
    game = get_object_or_404(Game, id=game_id)
    form = GameUpdateForm(instance=game)
    #form['category'] = game.category
    args = {
        'form' : form,
        'developer' : developer,
    }
    if request.method == 'POST':
        form = GameUpdateForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user.userprofile
            game.save()
            return redirect('game_description', game_id=game.id)
        else:
            args['form'] = form
            return render(request, 'game/edit_game.html', args)
    return render(request, 'game/edit_game.html', args)

    
