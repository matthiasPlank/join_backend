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
from django.views.decorators.csrf import csrf_protect



class CustomAuthToken(ObtainAuthToken):

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
     

def register_view(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data['email'])
        print(data['password'])
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
                    print(token)
                    loginSuccess = {
                        'token': token.key,
                        'user_id': user.pk,
                        'email': user.email, 
                        'username': user.username }
                    return JsonResponse(loginSuccess, safe=False)   
                return HttpResponse('No User')   
    return HttpResponse('No POST Request')

@csrf_protect
def check_token_view(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        print(data['token'])
        print(data['email'])