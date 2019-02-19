##############################################################
##### This view provides actions related to user account: ####
#####     * startpage                                     ####
#####     * login                                         ####
#####     * activate                                      ####
#####     * signup                                        ####
#####     * confirm_email                                 ####
#####     * set_password                                  ####
#####     * reset_password                                ####
#####     * logout_user                                   ####
#####     * edit_profile                                  ####
#####     * show_user                                     ####
#####     * show_agreement                                ####
#####     * report_successful_registration                ####
#####     * report_successful_restoring                   ####
#####     * report_successful_activation                  ####
##############################################################

from django.shortcuts import render, redirect
from gamestore.models import UserProfile
from gamestore.forms import (
    UserForm, 
    UserUpdateForm, 
    UserProfileUpdateForm,
    ChangePasswordForm,
    CustomPasswordResetForm,
    CustomPasswordSetForm,
)
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from gamestore.constants import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from ..tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.http import HttpRequest

def startpage(request):
    return render(request, BASE_HTML)

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = user
        resp = response
        birth_date = datetime.datetime.now() - datetime.timedelta(days=13*365) # 13 years by default
        User.objects.filter(username=user).update(first_name=response['first_name'],last_name=response['last_name'])
        user_object = User.objects.get(username=user)
        userProfile = UserProfile(
            user=user_object,
            birth_date=birth_date,
            gender='U'
        )
        userProfile.save()
        #user_auth = authenticate(username=username, password=password)
        user_auth = authenticate(username=user_object.username)
        request = HttpRequest()
        auth_login(request, user_auth)
    if profile is None:
        gender = 'F'
        #profile = UserProfile(
        #    user=user,
        #    birth_date=birth_date,
        #    gender=gender
        #)
        #profile.link = response.get('link')
        #profile.timezone = response.get('timezone')
        profile.save()
    return render(None, BASE_HTML, {'profile': profile, 'resp' : resp})

def login(request):
    ########## initial checks #############
    next_page = request.GET.get('next')
    if not next_page: #if request doesn't have ?next= parameter
        next_page = 'search_game' #keep search_game page as default redirect
    if request.user.is_authenticated:
        return redirect(next_page)
    else:
        ########  process post request  ##############
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is None:
                ########  report errors  ##########
                return render(request, LOGIN_HTML,
                              {'username': username, 'password': password,
                              'errors': "Your username or password was incorrect."})
            else:
                ########  login  ##################
                auth_login(request, user)
                return redirect(next_page)
        return render(request, LOGIN_HTML, {})

def restore_account(request):
    if request.user.is_authenticated:
        return redirect('search_game')
    else:
    ########  process post request  ##############
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            ########  check if user exists  ##############
            try:
                user_object = User.objects.get(username=username)
            except User.DoesNotExist:
                user_object = None
            if user_object:
                if not user_object.is_active:
                    ########  activate account and save ######
                    user_object.is_active = True
                    user_object.save()
                    user = authenticate(username=username, password=password)
                    if user:
                        user_object.is_active = False
                        user_object.save()
                        current_site = get_current_site(request)
                        mail_subject = 'Activate your old account.'
                        message = render_to_string(EMAIL_RESTORE_ACCOUNT_HTML, {
                            'user': user_object,
                            'domain': current_site.domain,
                            'uid':urlsafe_base64_encode(force_bytes(user_object.pk)).decode(),
                            'token':account_activation_token.make_token(user_object),
                        })
                        to_email = user_object.email
                        email = EmailMessage(mail_subject, message, to=[to_email])
                        email.send()
                        return redirect('restoring_success')
                    else:
                        ########  report errors  ##########
                        user_object.is_active = False
                        user_object.save()
                        args = {
                            'error' : "Incorrect password.",
                        }
                        return render(request, ACTIVATE_ACCOUNT_HTML, args)
                else:
                    args = {
                        'error' : "User is already active. Please login.",
                    }
                    return render(request, ACTIVATE_ACCOUNT_HTML, args)
            else:
            ########  user does not exist  ##############
                args = {
                    'error' : "User does not exist. Please sign up.",
                }
                return render(request, ACTIVATE_ACCOUNT_HTML, args)
    return render(request, ACTIVATE_ACCOUNT_HTML)

@transaction.atomic
def signup(request):
    if request.user.is_authenticated:
        return redirect('search_game')
    else:
    ########  process post request  ##############
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():

            ##  save valid form to User and UserProfile models  ##
                user = User.objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.clean_password2()
                )
                user.is_active = False
                user.save()
                userProfile = UserProfile(
                    user=user,
                    birth_date=form.cleaned_data['birth_date'],
                    gender=form.cleaned_data['gender']
                )
                userProfile.save()
                
                ####### send activation email ###########
                current_site = get_current_site(request)
                mail_subject = 'Activate your new account.'
                message = render_to_string(ACTIVATE_EMAIL_HTML, {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token':account_activation_token.make_token(user),
                })
                to_email = user.email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return redirect('registration_success')
            else:
            ########  report errors  ##########
                return render(request, SIGNUP_HTML, {'form': form})
        form = UserForm()
        return render(request, SIGNUP_HTML, {'form': form})

def confirm_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #log in user or not?
        #auth_login(request, user)
        return redirect('activation_success')
    else:
        return redirect('search_game')

def set_password(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect('profile')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = False
        user.save()
        setnewpasswordform = CustomPasswordSetForm(user=user)
        if request.method == 'POST':
            setnewpasswordform = CustomPasswordSetForm(data=request.POST, user=user)
            if setnewpasswordform.is_valid():
                setnewpasswordform.save()
                user.is_active = True
                user.save()
                return redirect('login')
            else:
                return render(request, SET_NEW_PASS_HTML, {'form': setnewpasswordform})
        else:
            setnewpasswordform = CustomPasswordSetForm(user=user)
            return render(request, SET_NEW_PASS_HTML, {'form': setnewpasswordform})
    else:
        return redirect('search_game')

def reset_password(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        feedback_message = 'If a user with that email is found in our system, you will be sent a password reset link.'
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            try:
                ####### send activation email ###########
                to_email = form.cleaned_data['email']
                user = User.objects.get(email=to_email)
                current_site = get_current_site(request)
                mail_subject = 'Reset your password.'
                message = render_to_string(EMAIL_RESET_PASS_HTML, {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user), #use the same hasing method as when activating user
                })
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return render(request, RESET_PASS_HTML, {'form': form, 'message': feedback_message})
            except ObjectDoesNotExist:
                return render(request, RESET_PASS_HTML, {'form': form, 'message': feedback_message})
        else:
             return render(request, RESET_PASS_HTML, {'form': form})
    form = CustomPasswordResetForm()
    return render(request, RESET_PASS_HTML, {'form': form})


@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('search_game')

@transaction.atomic
@login_required(login_url='/login/')
def edit_profile(request):

    ########  initialize variables  ##############
    user = request.user
    userprofile = user.userprofile
    username = user.username

    userform = UserUpdateForm(instance=user)
    profileform = UserProfileUpdateForm(instance=userprofile)
    changepasswordform = ChangePasswordForm(user=user)

    ########  prepare arguments  #################
    args = {
        'userform' : userform,
        'profileform' : profileform,
        'changepasswordform' : changepasswordform,
    }

    ########  process post request  ##############
    if request.method == 'POST':

        ########  update profile info  ###########
        if 'updateprofile' in request.POST:
            userform = UserUpdateForm(request.POST, instance=user)
            profileform = UserProfileUpdateForm(request.POST, instance=userprofile)
            if userform.data['username'] != username:
                userform.add_error('username', "You are not allowed to change your username")
                userform.errors['email'] = ""
                args['userform'] = userform
                return render(request, PROFILE_HTML, args)
            if userform.is_valid() and profileform.is_valid():
                userform.save()
                profileform.save()
                return redirect('profile')
            else:
                args['userform'] = userform
                args['profileform'] = profileform
                return render(request, PROFILE_HTML, args)

        ########  change password  ###############
        if 'changepassword' in request.POST:
            changepasswordform = ChangePasswordForm(data=request.POST, user=user)
            if changepasswordform.is_valid():
                changepasswordform.save()
                return redirect('profile')
            else:
                args['changepasswordform'] = changepasswordform
                return render(request, PROFILE_HTML, args)

        ########  delete user  ###################
        if 'deleteuser' in request.POST:
            user.is_active = False
            user.save()
            logout(request)
            return redirect('search_game')
    return render(request, PROFILE_HTML, args)

@login_required(login_url='/login/')
def show_user(request, user_id):

    ########  get user by id  ##########
    user = get_object_or_404(User, id=user_id)
    userprofile = user.userprofile

    ########  prepare arguments  #######
    args = {
        'user_info' : user,
        'userprofile' : userprofile,
    }
    return render(request, PROFILE_PREVIEW_HTML, args)


def show_agreement(request):
    return render(request, USER_AGREEMENT_HTML)

def report_successful_registration(request):
    args = {
        'thanks_for' : "registering",
        'message' : "Please, confirm your email before login.",
    }
    return render(request, THANKS_HTML, args)

def report_successful_restoring(request):
    args = {
        'thanks_for' : "restoring your account",
        'message' : "Please, confirm your email before login.",
    }
    return render(request, THANKS_HTML, args)

def report_successful_activation(request):
    args = {
        'thanks_for' : "activating your account",
        'message' : "Now you can login in our system.",
    }
    return render(request, THANKS_HTML, args)
