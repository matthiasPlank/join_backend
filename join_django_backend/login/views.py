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
from login.serializers import UserSerializer
from login.functions import getUsernameFromEmail, username_exists
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.contrib.auth.views import PasswordResetView
from rest_framework import viewsets


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



