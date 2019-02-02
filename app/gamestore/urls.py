from django.urls import re_path
from gamestore.views import account
from gamestore.views import game

urlpatterns = [
    re_path(r'^$', account.startpage, name='index'),
    re_path(r'^login/$', account.login, name='login'),
    re_path(r'^signup/$', account.signup, name='signup'),
    re_path(r'^logout/$', account.logout_user, name='logout_user'),
    re_path(r'^profile/$', account.profile, name='profile'),
    re_path(r'^search_game/$', game.search_game, name='search_game'),
    re_path(r'^my_games/$', game.show_my_games, name='my_games'),
    re_path(r'^games/(?P<game_id>[0-9]+)/$', game.game_description, name='game_description'),
    re_path(r'^uploaded_games/$', game.show_uploaded_games, name='uploaded_games'),
    re_path(r'^add_game/$', game.add_game, name='adding_game'),
    re_path(r'^edit_game/(?P<game_id>[0-9]+)/$', game.edit_game, name='editing_game'),
]