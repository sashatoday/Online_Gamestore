from django.shortcuts import render
from gamestore.models import User

def startpage(request):
    return render(request, "base.html", {})

def login(request):
    return render(request, "account/login.html", {})
    
def registration(request):
    return render(request, "account/registration.html", {})