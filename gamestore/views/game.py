#################################################
##### This view provides actions related     ####
##### to games:                              ####
#####     * search_game                      ####
#####     * apply_filter                     ####
#####     * show_my_games                    ####
#####     * show_wishlist                    ####
#####     * show_game_description            ####
#####     * play_game                        ####
#####     * buy_game                         ####
#################################################

from django.shortcuts import render, redirect
from gamestore.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
from gamestore.constants import *
from django.http import JsonResponse
from hashlib import md5
from django.core.exceptions import ObjectDoesNotExist
from gamestore.forms import SearchForm
from django.contrib.sites.shortcuts import get_current_site
from ..forms import calculate_age

def search_game(request):
    
    ###### get all games and apply filters #######
    games = Game.objects.all()
    form, games, search_applied = apply_filter(request, games)
    args = {
        'games' : games,
        'form' : form,
        'search_applied' : search_applied,
    }
    return render(request, SEARCH_GAME_HTML, args)

def apply_filter(request, games):

    if request.method == "POST":
        form = SearchForm(request.POST)
    else:
        form = SearchForm()
    search_applied = False
    
    ####### get filter values ###########
    if 'searchgame' in request.POST:
        search_applied = True
        search_key = request.POST.get('search_key', False)
        category = request.POST.get('category', False)
        filter = request.POST['sort_type']
        
        ####### get new list of games ###########
        if category == 'ALL':
            games = Game.objects.filter(name__icontains=search_key).order_by(filter)
        else:
            games = Game.objects.filter(name__icontains=search_key, category=category).order_by(filter)
    return form, games, search_applied

@login_required(login_url='/login/')
def show_my_games(request):

    ########  initialize variables  ##############
    user = request.user.userprofile

    ########  get list of purchased games ########
    purchased_games = Game.objects.filter(purchased_game__in=Purchase.objects.filter(buyer=user, complete=True))

    ########  apply filters  #####################
    form, purchased_games, search_applied = apply_filter(request, purchased_games)

    ########  prepare arguments  ################
    args = {
        'games' : purchased_games,
        'form' : form,
        'search_applied' : search_applied,
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

    ########  apply filters  #####################
    form, wished_games, search_applied = apply_filter(request, wished_games)

    ########  prepare arguments  ################
    args = {
        'games' : wished_games,
        'wishlist' : True,
        'form' : form,
        'search_applied' : search_applied,
    }
    return render(request, WISHLIST_HTML, args)

def show_game_description(request, game_id):

    ########  initialize variables  ##############
    if request.user.is_authenticated:
        user = request.user.userprofile
        anonym = False
    else:
        user = None
        anonym = True
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
    if user:
        if game.developer == request.user.userprofile:
            owner = True

    ########  check if purchased  ################
    purchased_game = False
    purchased_games = Game.objects.filter(purchased_game__in=Purchase.objects.filter(buyer=user, complete=True))
    if game in purchased_games:
        purchased_game = True

    ########  find scores  #######################
    scores = Score.objects.filter(game_in_score=game).order_by('-value')
    distinct_scores, scorers = [], []
    for score in scores:
        if score.scorer not in scorers:
            distinct_scores.append(score)
            scorers.append(score.scorer)
    

    ########  prepare arguments  #################
    args = {
        'game' : game,
        'owner' : owner,
        'anonym' : anonym,
        'purchased_game' : purchased_game,
        'scores' : distinct_scores[:10],
        'saved_game' : saved_game,
    }
    return render(request, GAME_DESCRIPTION_HTML, args)

@login_required(login_url='/login/')
def buy_game(request, game_id):
    user = request.user.userprofile
    game = get_object_or_404(Game, id=game_id) #return 404 if game not found
    birth_date = request.user.userprofile.birth_date
    age = calculate_age(birth_date)
    if age < game.age_limit:
        message = "You cannot buy this game. Age limit is: {}".format(game.age_limit)
        return render(request, BUY_GAME_HTML, {'message': message})
    if game.get_developer() == user:
        return redirect('play_game', game_id=game.id) #developers cannot buy their own games...
    try:
        purchase = Purchase.objects.get(buyer=user, purchased_game=game) #check if purchase is found
        if purchase.is_complete(): #if the purchase is already completed
            return redirect('play_game', game_id=game.id) #redirect user to the play game template
    except ObjectDoesNotExist: #no purchase found, lets create a new one :)
        purchase = Purchase(buyer=user, purchased_game=game) #create a new purchase
        purchase.save()
    pid = purchase.id #payment id (PID)
    amount = game.price
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest() #checksum is sent to payment service
    domain_url = get_current_site(request).domain
    args = {
        'pid': pid,
        'sid': sid,
        'amount': amount,
        'checksum': checksum,
        'game': game,
        'domain_url' : domain_url,
    }
    return render(request, BUY_GAME_HTML, args)
    
@login_required(login_url='/login/')
def play_game(request, game_id):

    ########## initialize variables #############
    user = request.user.userprofile
    game = get_object_or_404(Game, id=game_id)
    purchased_games = Game.objects.filter(purchased_game__in=Purchase.objects.filter(buyer=user, complete=True))
    owner = False
    if game.developer == user:
        owner = True
    if game not in purchased_games and not owner:
        return redirect('buying_game', game_id=game.id)
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
