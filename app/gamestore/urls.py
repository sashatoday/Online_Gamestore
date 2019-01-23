from django.urls import re_path
from gamestore.views import account
from gamestore.views import game

urlpatterns = [
    re_path(r'^$', account.startpage, name='index'),
    re_path(r'^login/$', account.login, name='login'),
    re_path(r'^signup/$', account.signup, name='signup'),
    re_path(r'^logout/$', account.logout_user, name='logout_user'),
    re_path(r'^uploaded_games/$', game.show_uploaded_games, name='uploaded_games'),
    re_path(r'^add_game/$', game.add_game, name='adding_game'),
]