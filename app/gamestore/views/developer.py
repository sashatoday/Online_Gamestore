#######################################################
##### This view provides actions related           ####
##### to developer actions:                        ####
#####     * show_uploaded_games                    ####
#####     * add_game                               ####
#####     * edit_game                              ####
#####     * show_statistics                        ####
#####     * show_agreement                         ####
#####     * report_successful_game_adding          ####
#######################################################

from django.shortcuts import render, redirect
from gamestore.models import *
from gamestore.forms import GameForm, GameUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from gamestore.constants import *
from django.db.models import Count, Sum
from gamestore.views.game import apply_filter

@login_required(login_url='/login/')
def show_uploaded_games(request):

    ########  initial checks  ####################
    if not request.user.userprofile.is_developer():
        return redirect('search_game')

    ########  get list of uploaded games  ########
    games = Game.objects.filter(developer=request.user.userprofile)

    ########  apply filters  #####################
    form, games, search_applied = apply_filter(request, games)

    ########  prepare arguments  #################
    args = {
        'games' : games,
        'form' : form,
        'search_applied' : search_applied,
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
        purchases = Purchase.objects.filter(purchased_game=game, complete=True).values_list('date').annotate(count=Count('pk')).order_by('date')
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

@login_required(login_url='/login/')
def show_agreement(request):

    ########  initial checks  ####################
    if not request.user.userprofile.is_developer():
        return redirect('search_game')

    return render(request, DEVELOPER_AGREEMENT_HTML)

@login_required(login_url='/login/')
def report_successful_game_adding(request):
    args = {
        'thanks_for' : "adding the game",
        'message' : "Now you can find your game in uploaded games.".format(request.POST.get('name', None)),
    }
    return render(request, THANKS_HTML, args)
