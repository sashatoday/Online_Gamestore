##########################################################
##### This view provides actions related to payments: ####
#####     * report_success                            ####
#####     * report_error                              ####
##########################################################

from django.shortcuts import render, redirect
from gamestore.models import Purchase, Game
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from gamestore.constants import *

@login_required(login_url='/login/')
def report_success(request):
    pid = request.GET.get('pid', None)
    ref = request.GET.get('ref', None)
    result = request.GET.get('result', None)
    checksum = request.GET.get('checksum', None)
    try:
        pid = int(pid)
        ref = int(ref)
    except ValueError:
        return redirect('payment_error')
    
    if pid and ref and result and checksum:
        game = get_object_or_404(Game, id=pid)
        user = request.user.userprofile
        purchase = Purchase.objects.filter(ref=ref) #check if purchase exists
        if purchase:
            return redirect('search_game')
        purchase = Purchase(buyer=user, purchasedGame=game, ref=ref)
        purchase.save()
        args = {
            'purchase': purchase,
            'game': game
        }
    else:
        return redirect('payment_error')
    return render(request, PAYMENT_SUCCESS_HTML, args)

@login_required(login_url='/login/')
def report_error(request):
    return render(request, PAYMENT_ERROR_HTML)
