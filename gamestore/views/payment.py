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
from hashlib import md5
from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url='/login/')
def report_success(request):
    pid = request.GET.get('pid', None)
    ref = request.GET.get('ref', None)
    result = request.GET.get('result', None)
    checksum = request.GET.get('checksum', None)
    if pid and ref and result and checksum: #at first just check that everything that we need exists
        try:
            purchase = Purchase.objects.get(id=pid, complete=False) #at first, we need to check if the purchase exists for this pid
            #if purchase is found, we need to compare the checksum sent from the payment service to here
            checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
            m = md5(checksumstr.encode("ascii"))
            checksum_ = m.hexdigest()
            #if checksum that we generated here is equal to the one sent from the payment service
            if checksum_ == checksum:
                purchase.complete = True
                purchase.ref = ref
                purchase.save()
                game = purchase.purchased_game
                args = {
                    'game': game
                }
                return render(request, PAYMENT_SUCCESS_HTML, args)
        except ObjectDoesNotExist:
            return redirect('payment_error')
    return redirect('payment_error')

@login_required(login_url='/login/')
def report_error(request):
    return render(request, PAYMENT_ERROR_HTML)
