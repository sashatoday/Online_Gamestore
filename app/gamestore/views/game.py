#######################################################
##### This view provides actions related to games: ####
#####     * search_game                            ####
#####     * show_my_games                          ####
#####     * show_wishlist                          ####
#####     * show_game_description                  ####
#####     * play_game                              ####
#####     * buy_game                               ####
#####     * show_uploaded_games (only developer)   ####
#####     * add_game (only developer)              ####
#####     * edit_game (only developer)             ####
#####     * show_statistics (only developer)       ####
#####     * report_successful_game_adding          ####
#######################################################

from django.shortcuts import render, redirect
from gamestore.models import *
from gamestore.forms import GameForm, GameUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
from gamestore.constants import *
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum
from hashlib import md5

def search_game(request):

    # TODO: process search input and filter objects
    games = Game.objects.all()
    args = {
        'games' : games,
    }
    return render(request, SEARCH_GAME_HTML, args)

@login_required(login_url='/login/')
def show_my_games(request):

    ########  initialize variables  ##############
    user = request.user.userprofile

    ########  get list of purchased games ########
    purchased_games = Game.objects.filter(purchased_game__in=Purchase.objects.filter(buyer=user))
    games = Game.objects.all()

    ########  prepare arguments  ################
    args = {
        'games' : purchased_games,
    }
    return render(request, MY_GAMES_HTML, args)

@login_required(login_url='/login/')
def show_wishlist(request):

    ########  initialize variables  ##############
    user = request.user.userprofile

    ####  check request to delete game from wishlist  ####
    if request.method == 'POST':
        game_id = request.POST['deletegame']
        game = WishList.objects.filter(wished_game=get_object_or_404(Game, id=game_id)).delete()

    ########  get list of wished games  ##########
    wished_games = Game.objects.filter(wished_game__in=WishList.objects.filter(potential_buyer=user))
    games = Game.objects.all()

    ########  prepare arguments  ################
    args = {
        'games' : wished_games,
        'wishlist' : True,
    }
    return render(request, WISHLIST_HTML, args)

@login_required(login_url='/login/')
def show_game_description(request, game_id):

    ########  initialize variables  ##############
    user = request.user.userprofile
    game = get_object_or_404(Game, id=game_id)

    ########  check wishlist  ####################
    saved_game = False
    wished_game = WishList.objects.filter(wished_game=game, potential_buyer=user)
    if wished_game:
        saved_game = True
    if request.method == 'POST':
        if 'wishlist' in request.POST:
            if not wished_game:
                wished_game = WishList.objects.create(potential_buyer=user, wished_game=game)
                wished_game.save()
                saved_game = True

    ########  check ownership  ###################
    owner = False
    if game.developer == request.user.userprofile:
        owner = True

    ########  check if purchased  ################
    purchased_game = False
    purchased_games = Game.objects.filter(purchased_game__in=Purchase.objects.filter(buyer=user))
    if game in purchased_games:
        purchased_game = True

    ########  find scores  #######################
    scores = Score.objects.filter(game_in_score=game)[:10]

    ########  prepare arguments  #################
    args = {
        'game' : game,
        'owner' : owner,
        'purchased_game' : purchased_game,
        'scores' : scores,
        'saved_game' : saved_game,
    }
    return render(request, GAME_DESCRIPTION_HTML, args)

@login_required(login_url='/login/')
def buy_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    purchase = Purchase.objects.filter(buyer=request.user.userprofile, purchased_game=game) #check if purchase exists
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
    return render(request, BUY_GAME_HTML, args)

@login_required(login_url='/login/')
def play_game(request, game_id):

    ########## initialize variables #############
    user = request.user.userprofile
    game = get_object_or_404(Game, id=game_id)
    purchased_games = Game.objects.filter(purchased_game__in=Purchase.objects.filter(buyer=user))
    owner = False
    if game.developer == user:
        owner = True
    if game not in purchased_games and not owner:
        return redirect('search_game')
    args = {
        'game' : game,
    }
    ########  process post request  ##############
    if request.is_ajax() and request.method == 'POST':
        data = json.loads(request.body)
        if data['type'] == 'SCORE': #save score, (game over)
            score = Score(value=data['score'], scorer=user, game_in_score=game)
            score.save()
            response = {'success':'true', 'message': 'Score saved.',}
        if data['type'] == 'SAVE': #save game state
            gamestate = GameState.objects.filter(player=user, game_in_state=game)
            if gamestate:
                gamestate.update(state=json.dumps(data['gameState']))
                response = {'success':'true', 'message': 'Gamestate updated.',}
            else:
                newgamestate = GameState(state=json.dumps(data['gameState']), player=user, game_in_state=game)
                newgamestate.save()
                response = {'success':'true', 'message': 'Gamestate created.',}
        return JsonResponse(response)

    if request.is_ajax() and request.method == 'GET': #load gamestate
        state = GameState.objects.filter(player=user, game_in_state=game)
        if state:
            gamestate = state.values('state')[0]['state']
            response = {'success':'true', 'message': 'Gamestate loaded!', 'state' : json.loads(gamestate),}
            return JsonResponse(response)
        else:
            response = {'success':'false', 'message': 'No gamestate found',}
            return JsonResponse(response)
        
    return render(request, PLAY_GAME_HTML, args)


####################################################################
#############  DEVELOPER FUNCTIONALITY ONLY  #######################
####################################################################

@login_required(login_url='/login/')
def show_uploaded_games(request):

    ########  initial checks  ####################
    if not request.user.userprofile.is_developer():
        return redirect('search_game')

    ########  get list of uploaded games  ########
    games = Game.objects.filter(developer=request.user.userprofile)

    ########  prepare arguments  #################
    args = {
        'games' : games,
    }
    return render(request, UPLOADED_GAMES_HTML, args)

@login_required(login_url='/login/')
def add_game(request):

    ########  initial checks   ###################
    if not request.user.userprofile.is_developer():
        return redirect('search_game')

    ########  prepare arguments  #################
    form = GameForm()
    args = {
        'form' : form,
    }
    ########  process post request  ##############
    if request.method == 'POST':
        form = GameForm(request.POST)

        if form.is_valid():
        ########  save game  ##############
            game = form.save(commit=False)
            game.developer = request.user.userprofile
            game.save()
            return redirect('adding_game_success')
        else:
        ########  report form errors  #####
            args['form'] = form
            return render(request, ADD_GAME_HTML, args)
    return render(request, ADD_GAME_HTML, args)

@login_required(login_url='/login/')
def edit_game(request, game_id):

    ########  initial checks  ####################
    if not request.user.userprofile.is_developer():
        return redirect('search_game')

    ########  initialize variables  ##############
    game = get_object_or_404(Game, id=game_id)
    form = GameUpdateForm(instance=game)
    args = {
        'form' : form,
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
            return render(request, EDIT_GAME_HTML, args)
    return render(request, EDIT_GAME_HTML, args)

@login_required(login_url='/login/')
def show_statistics(request):

    ########  initial checks  ####################
    if not request.user.userprofile.is_developer():
        return redirect('search_game')

    ########  get list of uploaded games  ########
    games = Game.objects.filter(developer=request.user.userprofile)
    games_data = []
    total_purchases = 0
    for game in games:
        ## get list of purchases for each game by date ##
        purchases = Purchase.objects.filter(purchased_game=game).values_list('date').annotate(count=Count('pk')).order_by('date')
        ## count the total number of purchases for the game ##
        total = purchases.aggregate(Sum('count'))['count__sum']
        if total:
            total_purchases += total
        else:
            total = 0
        data = {
            'game' : game,
            'purchases' : purchases,
            'total' : total,
        }
        games_data.append(data)

    ########  prepare arguments  #################
    args = {
        'games_data' : games_data,
        'total_purchases' : total_purchases,
    }
    return render(request, GAMES_STATISTICS_HTML, args)

def report_successful_game_adding(request):
    args = {
        'thanks_for' : "adding the game",
        'message' : "Now you can find your game in uploaded games.".format(request.POST.get('name', None)),
    }
    return render(request, THANKS_HTML, args)
