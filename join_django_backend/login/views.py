import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import authenticate, login , logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from login.functions import getUsernameFromEmail, username_exists
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.contrib.auth.views import PasswordResetView

from django.contrib.auth.forms import PasswordResetForm

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from django.core.mail import send_mail
from django.conf import settings


class CustomAuthToken(ObtainAuthToken):

    """
    CHECK login credentials and return Token
    """
    def post(self, request, *args, **kwargs):

        user = User.objects.get(email=request.data['email'])
        request.data['username'] = user.username
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        responseJSON = {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email, 
            'username': user.username
        }
        return HttpResponse(json.dumps(responseJSON), content_type='application/json')
     
"""
Register new User function
"""
def register_view(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        username = getUsernameFromEmail(data['email'])
        if username_exists(username):
                loginFailed = { 'wrongPassword' : False , 
                                'errorMessage' : 'User already exists' }
                return JsonResponse(loginFailed, safe=False)   
        else:
                user = User.objects.create_user(username, data['email'], data['password'])
                user.save()
                if user: 
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)
                    loginSuccess = {
                        'token': token.key,
                        'user_id': user.pk,
                        'email': user.email, 
                        'username': user.username }
                    return JsonResponse(loginSuccess, safe=False)   
                return HttpResponse('No User')   
    return HttpResponse('No POST Request')

"""
Check if user Token is valid
"""
def check_token_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(email=data['email'])
        userToken = Token.objects.get(user=user)
        if data['token'] == userToken.key: 
             return HttpResponse(True)
    return HttpResponse(False)


"""

"""
def reset_password_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email'] 
        print("Reset PASSWORD for " + email)
        return HttpResponse(False)
    
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = "Hello"
    email_plaintext_message = "Hello"

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()




