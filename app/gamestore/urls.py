from django.urls import re_path
from gamestore.views import account
from gamestore.views import game
from gamestore.views import payment

urlpatterns = [
    re_path(r'^$', account.startpage, name='index'),
    re_path(r'^login/$', account.login, name='login'),
    re_path(r'^signup/$', account.signup, name='signup'),
    re_path(r'^activate/$', account.activate, name='activate'),
    re_path(r'^logout/$', account.logout_user, name='logout_user'),
    re_path(r'^profile/$', account.profile, name='profile'),
    re_path(r'^user/(?P<user_id>[0-9]+)/$', account.show_user, name='user'),
    re_path(r'^search_game/$', game.search_game, name='search_game'),
    re_path(r'^my_games/$', game.show_my_games, name='my_games'),
    re_path(r'^games/(?P<game_id>[0-9]+)/$', game.show_game_description, name='game_description'),
    re_path(r'^play_game/(?P<game_id>[0-9]+)/$', game.play_game, name='play_game'),
    re_path(r'^uploaded_games/$', game.show_uploaded_games, name='uploaded_games'),
    re_path(r'^add_game/$', game.add_game, name='adding_game'),
    re_path(r'^edit_game/(?P<game_id>[0-9]+)/$', game.edit_game, name='editing_game'),
    re_path(r'^statistics/$', game.show_statistics, name='statistics'),
    re_path(r'^buy_game/(?P<game_id>[0-9]+)/$', game.buy_game, name='buying_game'),
    re_path(r'^payment/success/$', payment.success, name='payment_success'),
    re_path(r'^payment/error/$', payment.error, name='payment_error'),
]