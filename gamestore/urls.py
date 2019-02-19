from django.urls import re_path, include
from gamestore.views import account, game, payment, developer

urlpatterns = [

    re_path('', include('social_django.urls', namespace='social')),

### Base view
    re_path(r'^$', account.startpage, name='index'),

### Account
    re_path(r'^login/$', account.login, name='login'),
    re_path(r'^logout/$', account.logout_user, name='logout_user'),
    re_path(r'^facebook_signup/thanks/$', account.report_successful_facebook_signup, name='facebook_signup_seccess'),
    re_path(r'^signup/$', account.signup, name='signup'),
    re_path(r'^signup/thanks/$', account.report_successful_registration, name='registration_success'),
    re_path(r'^restore_account/$', account.restore_account, name='restore_account'),
    re_path(r'^restore_account/thanks/$', account.report_successful_restoring, name='restoring_success'),
    re_path(r'^thanks/$', account.report_successful_activation, name='activation_success'),
    re_path(r'^profile/$', account.edit_profile, name='profile'),
    re_path(r'^user/(?P<user_id>[0-9]+)/$', account.show_user, name='user'), # profile preview
    re_path(r'^confirm_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', account.confirm_email, name='confirm_email'),
    re_path(r'^reset_password/$', account.reset_password, name='reset_password'),
    re_path(r'^set_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', account.set_password, name='set_password'),
    re_path(r'^user_agreement/$', account.show_agreement, name='user_agreement'),

### Games
    re_path(r'^search_game/$', game.search_game, name='search_game'),
    re_path(r'^my_games/$', game.show_my_games, name='my_games'),
    re_path(r'^wishlist/$', game.show_wishlist, name='wishlist'),
    re_path(r'^games/(?P<game_id>[0-9]+)/$', game.show_game_description, name='game_description'),
    re_path(r'^buy_game/(?P<game_id>[0-9]+)/$', game.buy_game, name='buying_game'),
    re_path(r'^play_game/(?P<game_id>[0-9]+)/$', game.play_game, name='play_game'),

### Payments
    re_path(r'^payment/success/$', payment.report_success, name='payment_success'),
    re_path(r'^payment/error/$', payment.report_error, name='payment_error'),

### Developer functionality
    re_path(r'^add_game/$', developer.add_game, name='adding_game'),
    re_path(r'^add_game/thanks/$', developer.report_successful_game_adding, name='adding_game_success'),
    re_path(r'^edit_game/(?P<game_id>[0-9]+)/$', developer.edit_game, name='editing_game'),
    re_path(r'^uploaded_games/$', developer.show_uploaded_games, name='uploaded_games'),
    re_path(r'^statistics/$', developer.show_statistics, name='statistics'),
    re_path(r'^developer_agreement/$', developer.show_agreement, name='developer_agreement'),
]