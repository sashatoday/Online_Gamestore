from django.shortcuts import render, redirect
from gamestore.models import *
from gamestore.forms import GameForm, GameUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum

def search_game(request):
    developer = False
    if request.user.is_authenticated:
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
def show_wishlist(request):
    user = request.user.userprofile
    developer = user.is_developer()
    wished_games = WishList.objects.filter(potentialBuyer=user)
    games = Game.objects.all()
    args = {
        'games' : wished_games,
        'developer' : developer,
    }
    return render(request, "game/my_games.html", args)

@login_required(login_url='/login/')
def show_game_description(request, game_id):
    user = request.user.userprofile
    developer = user.is_developer()
    game = get_object_or_404(Game, id=game_id)
    owner = False
    if game.developer == request.user.userprofile:
        owner = True
    purchased_game = False
    purchased_games = Game.objects.filter(purchasedGame__in=Purchase.objects.filter(buyer=user))
    if game in purchased_games:
        purchased_game = True
    scores = Score.objects.filter(gameInScore=game)[:10]
    args = {
        'game' : game,
        'developer' : developer,
        'owner' : owner,
        'purchased_game' : purchased_game,
        'scores' : scores,
    }
    return render(request, "game/game_description.html", args)

@login_required(login_url='/login/')
def play_game(request, game_id):
    user = request.user.userprofile
    game = get_object_or_404(Game, id=game_id)
    purchased_games = Game.objects.filter(purchasedGame__in=Purchase.objects.filter(buyer=user))
    owner = False
    if game.developer == user:
        owner = True
    if game not in purchased_games and not owner:
        return redirect('search_game')
    developer = user.is_developer()
    args = {
        'game' : game,
        'developer' : developer,
    }
    if request.is_ajax() and request.method == 'POST':
        data = json.loads(request.body)
        if data['type'] == 'SCORE': #save score, (game over)
            score = Score(value=data['score'], scorer=user, gameInScore=game)
            score.save()
            response = {'success':'true', 'message': 'Score saved.', 'developer' : developer,}
        if data['type'] == 'SAVE': #save game state
            gamestate = GameState.objects.filter(player=user, gameInState=game)
            if gamestate:
                gamestate.update(state=json.dumps(data['gameState']))
                response = {'success':'true', 'message': 'Gamestate updated.', 'developer' : developer,}
            else:
                newgamestate = GameState(state=json.dumps(data['gameState']), player=user, gameInState=game)
                newgamestate.save()
                response = {'success':'true', 'message': 'Gamestate created.', 'developer' : developer,}
        return JsonResponse(response)

    if request.is_ajax() and request.method == 'GET': #load gamestate
        state = GameState.objects.filter(player=user, gameInState=game)
        if state:
            gamestate = state.values('state')[0]['state']
            response = {'success':'true', 'message': 'Gamestate loaded!', 'state' : json.loads(gamestate), 'developer' : developer,}
            return JsonResponse(response)
        else:
            response = {'success':'false', 'message': 'No gamestate found', 'developer' : developer,}
            return JsonResponse(response)
        
    return render(request, "game/play_game.html", args)


####################################################################
#############  DEVELOPER FUNCTIONALITY ONLY  #######################
####################################################################

@login_required(login_url='/login/')
def show_uploaded_games(request):
    developer = request.user.userprofile.is_developer()
    if not developer:
        return redirect('search_game')
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
        return redirect('search_game')
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
        return redirect('search_game')
    game = get_object_or_404(Game, id=game_id)
    form = GameUpdateForm(instance=game)
    args = {
        'form' : form,
        'developer' : developer,
    }
    if request.method == 'POST':
        if 'deletegame' in request.POST:
            game.delete()
            return redirect('uploaded_games')
        form = GameUpdateForm(request.POST, instance=game)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user.userprofile
            game.save()
            return redirect('game_description', game_id=game.id)
        else:
            args['form'] = form
            return render(request, 'game/edit_game.html', args)
    return render(request, 'game/edit_game.html', args)

@login_required(login_url='/login/')
def show_statistics(request):
    developer = request.user.userprofile.is_developer()
    if not developer:
        return redirect('search_game')

    games = Game.objects.filter(developer=request.user.userprofile)
    games_data = []
    total_purchases = 0
    for game in games:
        purchases = Purchase.objects.filter(purchasedGame=game).values_list('date').annotate(count=Count('pk')).order_by('date')
        total = purchases.aggregate(Sum('count'))['count__sum']
        if total:
            total_purchases += total
        else:

        data = {
            'name' : game.name,
            'purchases' : purchases,
            'total' : total,
        }
        games_data.append(data)

    args = {
        'games_data' : games_data,
        'total_purchases' : total_purchases,
        'developer' : developer,
    }
    return render(request, 'game/games_statistics.html', args)
