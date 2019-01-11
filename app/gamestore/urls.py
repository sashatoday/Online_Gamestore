from django.urls import re_path
from gamestore.views import account

urlpatterns = [
    re_path(r'^$', account.startpage, name='index'),
    re_path(r'^login/$', account.login, name='login'),
    re_path(r'^signup/$', account.signup, name='signup'),
    re_path(r'^logout/$', account.logout_user, name='logout_user'),
    re_path(r'^profile/$', account.profile, name='profile'),
]