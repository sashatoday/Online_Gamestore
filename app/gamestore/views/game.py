from django.shortcuts import render, redirect
from gamestore.models import UserProfile, Game
from gamestore.forms import GameForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def show_uploaded_games(request):
    user = UserProfile.objects.get(user=request.user)
    # CHECK LATER !!!!
    #if not user.is_developer():
    #    return redirect('index')
    games = Game.objects.filter(developer=user)

    return render(request, 'game/uploaded_games.html', {'games': games})
    
@login_required(login_url='/login/')
def add_game(request):
    user = UserProfile.objects.get(user=request.user)
    # CHECK LATER !!!!
    #if not user.is_developer():
    #    return redirect('index')
    if request.method == 'POST':
        form = GameForm(request.POST)
        try:
            if form.is_valid():
                game = form.save(commit=False)
                game.developer = user
                game.save()
            else:
                return render(request, 'game/add_game.html', {'form': form})
        except Exception:
            return render(request, 'game/add_game.html', {'form': form})
        else:
            #adding success, needs redirect
            return redirect('uploaded_games') # CHANGE REDIRECTED PAGE LATER!
    form = GameForm()
    return render(request, 'game/add_game.html', {'form': form})


    
