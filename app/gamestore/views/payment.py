from django.shortcuts import render, redirect
from gamestore.models import UserProfile, Purchase, Game
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required(login_url='/login/')
def success(request):
    pid = request.GET.get('pid', None)
    ref = request.GET.get('ref', None)
    result = request.GET.get('result', None)
    checksum = request.GET.get('checksum', None)
    try:
        pid = int(pid)
        ref = int(ref)
    except ValueError:
        return redirect('index')
    
    if pid and ref and result and checksum:
        game = get_object_or_404(Game, id=pid)
        user = request.user.userprofile
        purchase = Purchase.objects.filter(ref=ref) #check if purchase exists
        if purchase:
            return redirect('index')
        purchase = Purchase(buyer=user, purchasedGame=game, ref=ref)
        purchase.save()
        args = {
            'purchase': purchase,
            'game': game
        }
    else:
        return redirect('index')
    return render(request, 'payment/success.html', args)

@login_required(login_url='/login/')
def error(request):
    return render(request, 'payment/error.html')



