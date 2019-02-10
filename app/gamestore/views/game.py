#######################################################
##### This view provides actions related to games: ####
#####     * search_game                            ####
#####     * show_my_games                          ####
#####     * show_wishlist                          ####
#####     * show_game_description                  ####
#####     * play_game                              ####
#####     * show_uploaded_games (only developer)   ####
#####     * add_game (only developer)              ####
#####     * edit_game (only developer)             ####
#####     * show_statistics (only developer)       ####
#######################################################

from django.shortcuts import render, redirect
from gamestore.models import *
from gamestore.forms import GameForm, GameUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
from gamestore.core.constants import *
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum
from hashlib import md5

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

    ########  initialize variables  ##############
    user = request.user.userprofile
    developer = user.is_developer()

    ########  get list of purchased games ########
    purchased_games = Game.objects.filter(purchasedGame__in=Purchase.objects.filter(buyer=user))
    games = Game.objects.all()

    ########  prepare arguments  ################
    args = {
        'games' : purchased_games,
        'developer' : developer,
    }
    return render(request, "game/my_games.html", args)

@login_required(login_url='/login/')
def show_wishlist(request):

    ########  initialize variables  ##############
    user = request.user.userprofile
    developer = user.is_developer()

    ####  check request to delete game from wishlist  ####
    if request.method == 'POST':
        game_id = request.POST['deletegame']
        game = WishList.objects.filter(wishedGame=get_object_or_404(Game, id=game_id)).delete()

    ########  get list of wished games  ##########
    wished_games = Game.objects.filter(wishedGame__in=WishList.objects.filter(potentialBuyer=user))
    games = Game.objects.all()

    ########  prepare arguments  ################
    args = {
        'games' : wished_games,
        'developer' : developer,
        'wishlist' : True,
    }
    return render(request, "game/wishlist.html", args)

@login_required(login_url='/login/')
def show_game_description(request, game_id):

    ########  initialize variables  ##############
    user = request.user.userprofile
    developer = user.is_developer()
    game = get_object_or_404(Game, id=game_id)

    ########  check wishlist  ####################
    saved_game = False
    wished_game = WishList.objects.filter(wishedGame=game, potentialBuyer=user)
    if wished_game:
        saved_game = True
    if request.method == 'POST':
        if 'wishlist' in request.POST:
            if not wished_game:
                wished_game = WishList.objects.create(potentialBuyer=user, wishedGame=game)
                wished_game.save()
                saved_game = True

    ########  check ownership  ###################
    owner = False
    if game.developer == request.user.userprofile:
        owner = True

    ########  check if purchased  ################
    purchased_game = False
    purchased_games = Game.objects.filter(purchasedGame__in=Purchase.objects.filter(buyer=user))
    if game in purchased_games:
        purchased_game = True

    ########  find scores  #######################
    scores = Score.objects.filter(gameInScore=game)[:10]

    ########  prepare arguments  #################
    args = {
        'game' : game,
        'developer' : developer,
        'owner' : owner,
        'purchased_game' : purchased_game,
        'scores' : scores,
        'saved_game' : saved_game,
    }
    return render(request, "game/game_description.html", args)

@login_required(login_url='/login/')
def play_game(request, game_id):

    ########## initialize variables #############
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

    ########  process post request  ##############
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

    ########  initialize variables  ##############
    developer = request.user.userprofile.is_developer()
    if not developer:
        return redirect('search_game')

    ########  get list of uploaded games  ########
    games = Game.objects.filter(developer=request.user.userprofile)

    ########  prepare arguments  #################
    args = {
        'games' : games,
        'developer' : developer,
    }
    return render(request, 'game/uploaded_games.html', args)

@login_required(login_url='/login/')
def add_game(request):

    ########  initialize variables  ##############
    developer = request.user.userprofile.is_developer()
    if not developer:
        return redirect('search_game')
    form = GameForm()
    args = {
        'form' : form,
        'developer' : developer,
    }
    ########  process post request  ##############
    if request.method == 'POST':
        form = GameForm(request.POST)

        if form.is_valid():
        ########  save game  ##############
            game = form.save(commit=False)
            game.developer = request.user.userprofile
            game.save()
            return redirect('uploaded_games')

        else:
        ########  report form errors  #####
            args['form'] = form
            return render(request, 'game/add_game.html', args)
    return render(request, 'game/add_game.html', args)

@login_required(login_url='/login/')
def edit_game(request, game_id):

    ########  initialize variables  ##############
    developer = request.user.userprofile.is_developer()
    if not developer:
        return redirect('search_game')
    game = get_object_or_404(Game, id=game_id)
    form = GameUpdateForm(instance=game)
    args = {
        'form' : form,
        'developer' : developer,
    }
    ########  process post request  ##############
    if request.method == 'POST':

        if 'deletegame' in request.POST:
        ########  delete game  ##############
            game.delete()
            return redirect('uploaded_games')

        ########  save edited game  #########
        form = GameUpdateForm(request.POST, instance=game)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user.userprofile
            game.save()
            return redirect('game_description', game_id=game.id)

        else:
        ########  report form errors  #####
            args['form'] = form
            return render(request, 'game/edit_game.html', args)
    return render(request, 'game/edit_game.html', args)

@login_required(login_url='/login/')
def buy_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    purchase = Purchase.objects.filter(buyer=request.user.userprofile, purchasedGame=game) #check if purchase exists
    if purchase:
        return redirect('index')
    pid = game.id #payment ID
    amount = game.price
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest() #checksum is sent to payment service
    args = {
        'pid': pid,
        'sid': sid,
        'amount': amount,
        'checksum': checksum,
        'game': game
    }
    return render(request, 'game/buy_game.html', args)

@login_required(login_url='/login/')
def show_statistics(request):

    ########  initialize variables  ##############
    developer = request.user.userprofile.is_developer()
    if not developer:
        return redirect('search_game')

    ########  get list of uploaded games  ########
    games = Game.objects.filter(developer=request.user.userprofile)
    games_data = []
    total_purchases = 0
    for game in games:
        ## get list of purchases for each game by date ##
        purchases = Purchase.objects.filter(purchasedGame=game).values_list('date').annotate(count=Count('pk')).order_by('date')
        ## count the total number of purchases for the game ##
        total = purchases.aggregate(Sum('count'))['count__sum']
        if total:
            total_purchases += total
        else:
            total = 0
        data = {
            'name' : game.name,
            'purchases' : purchases,
            'total' : total,
        }
        games_data.append(data)

    ########  prepare arguments  #################
    args = {
        'games_data' : games_data,
        'total_purchases' : total_purchases,
        'developer' : developer,
    }
    return render(request, 'game/games_statistics.html', args)
