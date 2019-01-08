from django.urls import re_path
from gamestore.views import account

urlpatterns = [
    re_path(r'^$', account.startpage, name='index'),
    re_path(r'^login$', account.login, name='login'),
    re_path(r'^registration$', account.registration, name='registration'),
]